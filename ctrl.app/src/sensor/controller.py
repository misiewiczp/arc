### Sigrok PWM analyser
from sigrok.core.classes import *
import sys
from signal import *
import time
import lcm
from arc import control_t

# setup monitoring
context = Context.create()
for driver in context.drivers.values():
    if driver.name == 'fx2lafw':
        print('Using: ' + driver.name)

driver = context.drivers['fx2lafw']
driver_options = {}
devices = driver.scan(**driver_options)

if (len(devices) <> 1):
    print('Unexpected number of devices: ' + len(devices))
    sys.exit(1)

device = devices[0]
device.open()
# hardware connections
enabled_channels = set('D2,D4'.split(',')) # 3,5
for channel in device.channels:
    channel.enabled = (channel.name in enabled_channels)

session = context.create_session()
session.add_device(device)
session.start()
output = context.output_formats['csv'].create_output(device)

#initialize LCM
c_t = control_t()
lc = lcm.LCM()

#global zeros, ones, was_one, lasval, wave, learned, learned_cnt, emit_lcm

zeros = [0,0]
ones = [0,0]
was_one = [True, True]
lastval = [-1, -1]
wave = [0,0]
emitevery = 10
learn_till = 10
learned = [0,0]
learned_cnt = [0,0]
emit_lcm = [False,False]

def calc_pwm(idx, val):

    if lastval[idx] != val and val == '1':
        wave[idx] += 1
        if (wave[idx] % emitevery) == 0 and (wave[idx] > learn_till):
#            print ("{}\t{}\t{},{},{}".format( round(zeros-learned), ones, zeros, ones+zeros, float(ones)/float(ones+zeros)))
#            print ("{} - {}\t{}\t\t{}\t{}".format( idx, wave[idx], round(ones[idx]-learned[idx]), ones[idx], zeros[idx]))
            if idx == 0:
                c_t.motor = round(ones[idx]) #float(ones[idx])/float(ones[idx]]+zeros[idx]) # round( (float(ones[0])/float(learned[0])-1)*30 ) #/float(ones[0]+zeros[0])*100
                emit_lcm[0] = True
            else:
                c_t.servo = round(ones[idx]) #float(ones[idx])/float(ones[idx]]+zeros[idx]) # round( (float(ones[1])/float(learned[1])-1)*30 )
                emit_lcm[1] = True
            
        if wave[idx] <= learn_till and was_one[idx]:
            learned[idx] += ones[idx]
            learned_cnt[idx] += 1
        if wave[idx] == learn_till:
            learned[idx] = round(float(learned[idx])/float(learned_cnt[idx])) #avg number of ones per session
            print("Learned: {}".format(learned[idx]))

        ones[idx] = 0
        zeros[idx] = 0
        was_one[idx] = True
    
    lastval[idx] = val
    if val == '0':
        zeros[idx] += 1
    else:
        ones[idx] += 1



def datafeed_in(device, packet):
    global emit_lcm
    text = output.receive(packet)
    for data in text.split("\n"):
        if len(data) < 5:
            continue
        calc_pwm(0, data[2])
        calc_pwm(1, data[4])
        if emit_lcm[0] and emit_lcm[1]: #change
            if (time.time() > c_t.timestamp):
                c_t.timestamp = time.time()
                lc.publish('CTRL', c_t.encode())
            emit_lcm = [False, False]


session.add_datafeed_callback(datafeed_in)

signal(SIGINT, lambda signum, frame: session.stop())

session.run()

device.close()


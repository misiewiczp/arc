
class Command(object):

    finished = True
    cancelled = False

    # continue ?
    def run:
        finished = False

    def is_finished:
        return finished

    def cancel:
        cancelled = True

class Stop(Command):

    def run:
        set_servo(0)
        set_motor(0)
        finished = True


class Turn(object):

    angle = 0
    turned = 0
    lastTime = 0

    def __init__(self, angle):
       self.angle = angle
       self.turned = 0


    def run:
        if self.angle > 0:
            lastTime = time.time()
            lcm.subscribe("IMU", lambda i_t: self.run_update(i_t))
            set_servo(100)
            set_motor(30)

    def run_update(i_t):
        diff = i_t.time - lastTime
        last_Time = i_t.time
        turned = turned + i_t.omega*diff
        if (self.angle < self.turned):
            set_servo(0)
            set_motor(0)
    
    def calc_motor_servo(currServ, curr_Moto, currTurn, tgtTurn):
        return (0,0)




class PlanningCommand(Command):

    currentCommand = None

    def run:
        plan = calc_plan()
        for cmd in enumerate(plan):
            self.currentCommand = cmd
            cmd.run()
            if self.cancelled:
                break

        finished = True
        return False

    def calc_plan:
        return ()

    def cancel:
        self.cancelled = True
        if self.currentCommand != None:
            self.currentCommand.cancel()


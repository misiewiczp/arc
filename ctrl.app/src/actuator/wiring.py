import wiringpi as wp

wp.wiringPiSetupGpio()
wp.pwmSetMode(wp.PWM_MODE_MS);
wp.pwmSetRange (1000);
#wp.pwmSetClock(384); #50Hz
wp.pwmSetClock(302); #63Hz

wp.pinMode(13, wp.PWM_OUTPUT)      # pwm only works on GPIO port 18 
wp.pwmWrite(13, 28)    # 

wp.pinMode(18, wp.PWM_OUTPUT)      # pwm only works on GPIO port 18 
wp.pwmWrite(18, 28)    # 

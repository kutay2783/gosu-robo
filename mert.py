import Adafruit_BBIO.PWM as PWM
pwmC="P8_13"
pwmS=13
PWM.start(pwmC,pwmS,50,0)
while(1)
	pwmS=input('Enter PWM: ')
	if pwmS="q":
		break
	else:
		PWM.set_duty_cycle(pwmC,pwmS)

PWM.stop(pwmC)
#PWM.cleanup()

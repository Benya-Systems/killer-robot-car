import RPi.GPIO as GPIO


from time import sleep


class Mover:
        
    def __init__(self):
        
        # Pins for Motor Driver Inputs 
        self.Motor1A = 22
        self.Motor1B = 27
        self.Motor1E = 4

        self.Motor2A = 23
        self.Motor2B = 24
        self.Motor2E = 25
        self.pwm1A=None
        self.pwm2A=None
        self.setupGPIOPins()


    def setupGPIOPins(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)              # GPIO Numbering
        GPIO.setup(self.Motor1A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(self.Motor1B,GPIO.OUT)
        GPIO.setup(self.Motor1E,GPIO.OUT)
        GPIO.setup(self.Motor2A,GPIO.OUT)  # All pins as Outputs
        GPIO.setup(self.Motor2B,GPIO.OUT)
        GPIO.setup(self.Motor2E,GPIO.OUT)
        self.pwm1A = GPIO.PWM(self.Motor1E,100)
        self.pwm2A = GPIO.PWM(self.Motor2E,100)
        

    
    def configurePWM(self,movementDir):

        if movementDir == 'f':
            self.pwm1A.start(90)
            self.pwm2A.start(90)
        elif movementDir == 'r':
            self.pwm1A.start(90)
            self.pwm2A.start(50)
        elif movementDir == 'l':
            self.pwm1A.start(50)
            self.pwm2A.start(90)
        elif movementDir == 's':
            self.pwm1A.stop()
            self.pwm2A.stop()

    def move(self,movementDir):


        movementDir='f' #input()
        self.configurePWM(movementDir)
        if movementDir == 'f':

            GPIO.output(self.Motor1A,GPIO.HIGH)
            GPIO.output(self.Motor1B,GPIO.LOW)
            GPIO.output(self.Motor1E,GPIO.HIGH)
        
            GPIO.output(self.Motor2A,GPIO.HIGH)
            GPIO.output(self.Motor2B,GPIO.LOW)
            GPIO.output(self.Motor2E,GPIO.HIGH)
        
            #print("Going forwards")
            
        elif movementDir == 'r':

            GPIO.output(self.Motor1A,GPIO.HIGH)
            GPIO.output(self.Motor1B,GPIO.LOW)
            GPIO.output(self.Motor1E,GPIO.HIGH)
        
            GPIO.output(self.Motor2A,GPIO.HIGH)
            GPIO.output(self.Motor2B,GPIO.LOW)
            GPIO.output(self.Motor2E,GPIO.HIGH)

        elif movementDir == 'l':
     
            GPIO.output(self.Motor1A,GPIO.HIGH)
            GPIO.output(self.Motor1B,GPIO.LOW)
            GPIO.output(self.Motor1E,GPIO.LOW)
        
            GPIO.output(self.Motor2A,GPIO.HIGH)
            GPIO.output(self.Motor2B,GPIO.LOW)
            GPIO.output(self.Motor2E,GPIO.HIGH)

        # Stop
        elif movementDir == 's':
            GPIO.output(self.Motor1E,GPIO.LOW)
            GPIO.output(self.Motor1B,GPIO.LOW)
            GPIO.output(self.Motor2E,GPIO.LOW)
            GPIO.output(self.Motor2B,GPIO.LOW)
            #print("Stop")

        # self.pwm1A.stop()
        # self.pwm2A.stop()
        
    def destroyGPIOPins(self):  
        GPIO.cleanup()

# 
# if __name__ == '__main__':     # Program start from here
#     setup()
#     try:
#             loop()
#     except KeyboardInterrupt:
#         destroy()

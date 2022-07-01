import RPi.GPIO as GPIO
import time

#Pines Elevacion
in1 = 17
in2 = 18
in3 = 27
in4 = 22

#Pines Azimuth
in11 = 23
in22 = 24
in33 = 10
in44 = 9

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in11, GPIO.OUT )
GPIO.setup( in22, GPIO.OUT )
GPIO.setup( in33, GPIO.OUT )
GPIO.setup( in44, GPIO.OUT )
 
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in11, GPIO.LOW )
GPIO.output( in22, GPIO.LOW )
GPIO.output( in33, GPIO.LOW )
GPIO.output( in44, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

motor_pins1 = [in11,in22,in33,in44]
motor_step_counter1 = 0 ;


def low():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in11, GPIO.LOW )
    GPIO.output( in22, GPIO.LOW )
    GPIO.output( in33, GPIO.LOW )
    GPIO.output( in44, GPIO.LOW )

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in11, GPIO.LOW )
    GPIO.output( in22, GPIO.LOW )
    GPIO.output( in33, GPIO.LOW )
    GPIO.output( in44, GPIO.LOW )
    GPIO.cleanup() 


while True:
    try:
        angle = float(input('Ingrese un angulo entre 0 y 90, para la elevacion: '))
        angle1 = float(input('Ingrese un angulo entre 0 y 360 : '))

        if (angle1>0):
            step_count1 = int(angle1*2*65*1/5.625)
            direction1 = True
        elif (angle1<0):
            step_count1 = int(-1*angle1*2*65*1/5.625)
            direction1 = False
        elif(angle1==0):
            step_count1=0


        if (angle>0):
            step_count = int(angle*2.4*64*1/5.625)
            direction = True
        elif (angle<0):
            step_count = int(-1*angle*2.4*64*1/5.625)
            direction = False
        elif(angle==0):
            step_count=0
        
        i = 0
        for i in range(step_count):
            for pin in range(0, len(motor_pins)):
                GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
            if direction==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif direction==False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else: # defensive programming
                print( "uh oh... direction should *always* be either True or False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )

        j = 0
        for j in range(step_count1):
            for pin in range(0, len(motor_pins1)):
                GPIO.output( motor_pins1[pin], step_sequence[motor_step_counter1][pin] )
            if direction1==True:
                motor_step_counter1 = (motor_step_counter1 - 1) % 8
            elif direction1==False:
                motor_step_counter1 = (motor_step_counter1 + 1) % 8
            else: # defensive programming
                print( "uh oh... direction should *always* be either True or False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )
        motor_step_counter1 = 0 ;
        motor_step_counter = 0 ;
        low();
        
        
    except e as Exception:
        print(e)
        cleanup()
        exit(1)
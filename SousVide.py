"""
SousVide.py

This program creates a user interface to a PID/Phase angle controlled heating element

Authors: John Lucero and Katie Ayala
Date: 12/8/2018
Version 2.0 
"""

import time
import os
import RPi.GPIO as GPIO
from threading import Thread
from w1thermsensor import W1ThermSensor
import PID
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import numpy as np

#Set GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) #output for relay
GPIO.setup(16, GPIO.OUT)#output to fire TRIAC
GPIO.setup(5, GPIO.IN)  #input for Zero Crossing 
#GPIO button assinments
enter = 18
back = 17
up = 27
down = 22
#GPIO inputs are set as pull up will only read False or 0 when the button is pressed
GPIO.setup(enter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(back, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO 23 is used by the temperature sensor

#####
# Declare and Initialize Variables
#####
global fireDelay  #Used to hold a float indicating how long to wait after zero crossing before fireing the TRIAC
global pulseWidth #Used to hold a float indicating how indicating how long to bias the TRIACs gate
global temp       #Used to hold a float representing the temperature of the water from the temperature sensor
global ZC         #Bool used to indicate if a zero crossing has occured
global check      #Used to hold a string to indicate what safety question is being asked
global water      #Bool used to indicate the presence of water
global pump       #Bool used to indicate if the pump has been primed
global setTemp    #Used to hold an int representing the useres desired temperature
global nTemp      #Used to hold a temprature during selection
global i          #This is an int used as a count to trigger display events

#Set bool safety checks to False
water = False #water is a bool used for a safety check
pump = False  #pump is a bool used for a safety check
run = False   #run is a boolean value that will prevent the PID and heater loops from executing if False
yN = ['Yes', 'No'] #An array holding string values for user input
tempRange = np.arange(100,213) #An array holding ints of the operational temprature range
counter = 0 #counter is initially used to index the yN array
setTemp = 0 #initial set temperature is set to 0 for safety
nTemp = 100 #Initializing this at 100 will start the displayed set temp at 100
temp = 0
fireDelay = 0.008

#Variables to set the PID coefficents
kp = 0.25 #proportional
ki = 0    #intergral
kd = 0    #differential

#Initialize a PID instance
pid = PID.PID(kp, ki, kd, 0, 1) 
pid.set_output_limits(100, 212)

#Initialize the Temperature Sensor
sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "00000a29a4dd")

#Example on how to use sensor
#temp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
#print("This is the current temperature: %.2f Degrees F." %temp) 
 
###############################################################################

#Configuration values for display use
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

font = ImageFont.truetype("arial.ttf", 14, encoding="unic")
font2 = ImageFont.truetype("arial.ttf", 32, encoding="unic")

###############################################################################

#################################################
#                   FUNCTIONS                   #
#################################################

#The invert function is used to invert the pixel value for a line of text
#   acting as a highlight
def invert(draw,x,y,text): 
    draw.rectangle((x, y, x+120, y+15), outline=255, fill=255)
    draw.text((x, y), text, font=font, outline=0, fill=0)
	
#yesNoWater functon uses the OLED display to ask the user if
#   water is present. 
def yesNoWater(disp, draw, menustr,index):
    global check
    global yNindex
    check = "water"
    #code to draw is there water question
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((0, 0), "Is there water?",  font=font, fill=255)
    for i in range(len(menustr)):
        if (i == index):
            yNindex = i
            invert(draw, 2, (i*15)+34, menustr[i]) 
        else:
            draw.text((2, (i*15)+34), menustr[i], font=font, fill=255)
    disp.image(image)
    disp.display()
    
#yesNoPump function useds the OLED display to ask the user is
#   the water pump was primed... It can't pump air.
def yesNoPump(disp, draw, menustr,index):
    global yNindex
    global check
    check = "pump"
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.multiline_text((0,0), "Is the pump \nprimed?", font=font, fill=255, spacing=5, align='left')
    for i in range(len(menustr)):
        if (i == index):
            yNindex = i
            invert(draw, 2, (i*15)+34, menustr[i])
        else:
            draw.text((2, (i*15)+34), menustr[i], font=font, fill=255)	
    disp.image(image)
    disp.display()

#yN_operation uses if statements to evaluate user input to determine
#   if the water or pump bool values should be set to True.
def yN_operation(strval):
    global yNindex
    global check
    global water
    global pump
    global counter
    if (strval == "Yes" and  check == "water"):
        water = True
        print('water was set to:', water, ".")
        yesNoPump(disp, draw, yN, counter%2)
        strval = "no"
		#pass
    if (strval == "Yes" and  check == "pump"):
        pump = True
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.image(image)
        disp.display()
        print('pump was set to:', pump, ".")
        pass
    if (strval == "No" and check == "water"):
        water = False
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((0, 0), "Please add water",  font=font, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(5)
        yesNoWater(disp, draw, yN, counter%2) 
    if (strval == "No" and check == "pump"):
        pump = False
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.multiline_text((0,15), "Please prime the \npump", font=font, fill=255, spacing=0, align='left')
        disp.image(image)
        disp.display()
        time.sleep(5)
        yesNoPump(disp, draw, yN, counter%2) 
        

#enter_callback is called when the enter button is pressed to determine a selection
#The selection is set to the variable strval then passes to the yN_operation function
def enter_callback(channel):  
    global yNindex
    print("enter")
    strval = yN[yNindex]
    yN_operation(strval)
    print(strval)

#up_callback is called when the up button is pressed. It increments a counter and calls
#   the appropiate safety question passing the counter to index the yN array                
def up_callback(channel):
    global counter
    if GPIO.input(up) == 0:
        counter -= 1
    #print(counter) #for debugging   
    #print("up")    #for debugging
    if (check == "water"):
        yesNoWater(disp, draw, yN, counter%2)
    else:
        yesNoPump(disp, draw, yN, counter%2)     
    disp.image(image)
    disp.display()   

#down_callback is called when the down button is pressed. It decreases the counter and calls
#   the appropiate safety question passing the counter to index the yN array       
def down_callback(channel):
    global counter
    if GPIO.input(down) == 0:
        counter += 1
    #print(counter) #for debugging
    #print("down")  #for debugging  
    
    if (check == "water"):
        yesNoWater(disp, draw, yN, counter%2)
    else:
        yesNoPump(disp, draw, yN, counter%2)   
    disp.image(image)
    disp.display() 

#newTemp accepts and array for the menustr and an integer to index that array
#   setting nTemp to the indexed value
def newTemp(disp, draw, menustr,index):
    global tempRange
    global nTemp
    nTemp = menustr[index]
    print("This is nTemp:", nTemp,".")

#enter_callback sets, setTemp equal to the displayed temp
#   also i is set to 0
def enter_callback2(channel):  
    global nTemp
    global setTemp
    global i
    setTemp = nTemp
    i = 0

"""
While loops are used in up_callback2 and down_callback2 to permit scrolling when the button 
is held down. The scrolling rate is determined by the sleep time, no numerical values are 
skipped regardless of rate. However scroll rates approaching and over 5Hz will cause the 
values displayed on the screen to skip because the scroll rate superceeds the refresh rate. 
Slightly faster scroll rate may be possible if the I2C clock rate was increased.
"""
                
#up_callback2 increments counter and sets the i to 1
def up_callback2(channel):
    global counter
    global setTemp
    global i
    while not GPIO.input(27):
        if counter <= 112:
            counter += 1
        else: 
            counter = 0
        #print(counter) #used for debugging
        i = 1
        newTemp(disp, draw, tempRange, counter) 
        time.sleep(0.2)

#down_callback2 decreases the countrer and sets i to 1
def down_callback2(channel):
    global counter
    global setTemp
    global i
    while not GPIO.input(down):
        if counter >= 0:
            counter -= 1
        else: 
            counter = 112
        i = 1
        newTemp(disp, draw, tempRange, counter)           
        time.sleep(0.65)

#acControl is a function intended to run as a thread. This thread is responsible
#	for controlling the power applied to the heating element based off the PID output.
def acControl():
    global ZC
    global fireDelay
    global pulseWidth
    global run
    print("AC controll thread is running")
    ZC = False
    #zeroCrossing setes ZC to true when the sine wave of the input power
    #crosses zero potential.
    def zeroCrossing(channel):
        global ZC
        ZC = True
    
    #Interupt for the zero crossing
    GPIO.add_event_detect(5, GPIO.FALLING, callback = zeroCrossing) 
    #This while loop uses ZC to reference the begining of a half wave
    while run:
        if ZC == True:
            if fireDelay > 0.007:
                ZC = False
            else:
                time.sleep(fireDelay) #length of time to wait before fireing 
                GPIO.output(16, 1)
                time.sleep(0.000250)  #250us should be long enough to fire the Triac
                GPIO.output(16, 0)
                ZC = False
    print("\nAC Controll thread is quitting")

#runningDisplay is a function intended to run as a thread. This thread is resposible
#	for updating the information displayed during operation. 
def runningDisplay(dispTemp):
    global temp
    global nTemp
    global run
    global i
    global counter
    print("Display thread is running!")
    i = 1
    while run:
        draw.rectangle((0,0,width,height), outline=0,fill=0)
        if (not nTemp == setTemp) and (not i == 0):
                dTemp = nTemp
                draw.text((5,0),"Select Temp %d\u00b0F" %dTemp, font=font, fill=255)
                draw.text((0, 15), "Hit Enter to Confirm!", font=font, fill=255)
                i += 1
                if i == 20:
                    i = 0
                    counter = setTemp - 100
                   #print("Counter: ", counter)
        else:
            dTemp = setTemp
            draw.text((10,0),"Set Temp %d\u00b0F" %dTemp, font=font, fill=255)
            draw.text((18,15),"Current Temp", font=font, fill=255)
        draw.text((8, 32), "%5.1f\u00b0F" %temp, font=font2, fill=255)
        disp.image(image)
        disp.display()
        time.sleep(0.05) #original sleep was 0.1
        #print("This is i: ", i)
    print("\nDisplay thread is quitting")

#temperature is intended to run as a thread. It is responsible for 
#	updating the temp variable with current sensor reading. 
def temperature():
    global temp
    global run
    print("temp theread is running!")
    while run:
        temp = float(sensor.get_temperature(W1ThermSensor.DEGREES_F))
        time.sleep(0.5)
    print("\nTemp Thread is quitting")

def readConfig ():
    with open ('/tmp/pid.conf', 'r') as f:
        config = f.readline().split(',')
        pid.set_tunings (float(config[0]), float(config[1]), 
                        float(config[2]))

def createConfig ():
    if not os.path.isfile('/tmp/pid.conf'):
        with open ('/tmp/pid.conf', 'w') as f:
            f.write('%s,%s,%s'%(kp, ki, kd))
createConfig()


#The following are interrupts used to call functions when the corrasponding button is pressed
GPIO.add_event_detect(enter, GPIO.FALLING , callback=enter_callback, bouncetime=350)
#GPIO.add_event_detect(back, GPIO.FALLING , callback=back_callback, bouncetime=500) #the back button isn't used
GPIO.add_event_detect(up, GPIO.FALLING , callback=up_callback, bouncetime=350)
GPIO.add_event_detect(down, GPIO.FALLING , callback=down_callback, bouncetime=350) 

##################################################
#                      MAIN                      #
##################################################

"""
Part 1 Prompts the user with questions designed 
to prohibit unsafe operation of the Sous Vide   
"""

#Calling the yesNoWater functions draws the initial display
#	and begins a logic loop that can only be exited 
#	when the safety questions have been answered correctly
yesNoWater(disp, draw, yN, counter%2)

#This while loop keeps part 2 from executing until
#	run is set to True signaling it is safe to operate
#	both the heater and pump
while True:
    if (water and pump):
        run = True
        print("Run is", run,".")
        break
    time.sleep(2) #arbitray sleep value to slow time to the next iteration

"""
Part 2 Deals with Sous Vide operation only once
water and pump have been set to True
"""

#Remove the old event detects definitions so new ones can be set without error
GPIO.remove_event_detect(enter) 
GPIO.remove_event_detect(up)
GPIO.remove_event_detect(down)

counter = 0 #Reset the counter to 0 so it can be used to properly index the begining of the tempRange array

#New set of interrupts to call appropriate functions during Sous Vide operation
GPIO.add_event_detect(enter, GPIO.FALLING , callback=enter_callback2, bouncetime=350)
#GPIO.add_event_detect(back, GPIO.FALLING , callback=back_callback, bouncetime=500)
GPIO.add_event_detect(up, GPIO.FALLING , callback=up_callback2, bouncetime=350)
GPIO.add_event_detect(down, GPIO.FALLING , callback=down_callback2, bouncetime=350) 

#Start the pump
if run == True:
    print("Starting the pump!")
    GPIO.output(4, 1)  #this will turn on the pump
    #time.sleep(20)    #used during debugging
    #GPIO.output(4, 0) #used during debugging
        
#def pidThread(run, set_point, processVar)
#   while run:
#       pid.set_point = set_point
#       PIDout = pid.compute(processVar)
#    return PIDout

#GPIO.add_event_detect(5, GPIO.FALLING, callback = zeroCrossing) 

#Start Threads for the phase angle control, tempurature reading and display
t1 = Thread(target = acControl)
t2 = Thread(target = temperature)
t3 = Thread(target = runningDisplay, args = (temp,))
t1.start()
t2.start()
t3.start()

print("Press ctrl-c to exit")
try:
    while run:
        readConfig()
        pid.set_point = setTemp + 0.5
        PIDout = pid.compute(temp)
        fireDelay = 0.00833 - ((PIDout - 100) * 0.0652)/1000.0 #Use 0.0741 for full output and 0.0652 for 1062W
        print("The current temp is %.2f F, PID out %.2f fireDelay: %.5fs" %(temp, PIDout, fireDelay))
        time.sleep(1)
except KeyboardInterrupt:
    pass

run = False
GPIO.output(4, 0)
time.sleep(2)
draw.rectangle((0,0,width,height), outline=0,fill=0)
disp.image(image)
disp.display()
time.sleep(2)
GPIO.cleanup()
print("Exiting...")

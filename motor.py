print("\nInitializing...\n")

# CONTROLLER SETTINGS
Button_Pin = 18 #GPIO
Button_HIGH_Pin = 19 #GPIO
PWM_Pin = 13 #GPIO
PWM_Freq = 20000 #Hz
PWM_Start = 10 #%
Ramp_Up_Time = 10 #sec
Ramp_Down_Time = 10 #sec

# Imports
from machine import Pin
from machine import PWM
from time import sleep
from primitives import Pushbutton
import uasyncio as asyncio

# Set PWM pins and settings
pwm_motor = PWM(Pin(PWM_Pin)) # PWM pin
pwm_motor.freq(PWM_Freq) # PWM frequency
pwm_motor.duty_u16(0) # Makes sure PWM is at minimum

# Set button pins
button = Pin(Button_Pin, Pin.IN, Pin.PULL_DOWN) # Sense pin
high = Pin(Button_HIGH_Pin, Pin.OUT) # High pin
high.on()

# Math to pass settings to PWM controls
PWM_start_val = (PWM_Start / 100) * 65535 # Converts start percentage to a usable integer
PWM_int_up = (65535 - PWM_start_val) // (Ramp_Up_Time * 100) # Calculates step size to meet ramp up time
PWM_int_dn = -(65535 // (Ramp_Down_Time * 100)) # Calculates step size to meet ramp down time

state = 0
press = False

def push():
    print("\n-----Pushed-----")
    global state
    global press
    press = True
    if state == 0:
        state = 1
    elif state == 1:
        state = 0

async def motor():
    global press
    exit = False
    while True:
        if press == True:
            press = False
            if state == 1:
                print("\nStarting motor...")
                if exit == True:
                    duty_start = duty_mem
                    exit = False
                elif exit == False:
                    duty_start = PWM_start_val
                for duty in range(duty_start, 65535, PWM_int_up):
                    if press == True:
                        duty_mem = duty
                        exit = True
                        break
                    #print(duty)
                    pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
                if exit != True:
                    print("\n-----FULL ON-----")
                    pwm_motor.duty_u16(65535)
                    await asyncio.sleep_ms(5)
            elif state == 0:
                print("\nStopping motor...")
                if exit == True:
                    duty_start = duty_mem
                    exit = False
                elif exit == False:
                    duty_start = 65535
                for duty in range(duty_start, 0, PWM_int_dn):
                    if press == True:
                        duty_mem = duty
                        exit = True
                        break
                    #print(duty)
                    pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
                if exit != True:
                    print("\n-----FULL OFF-----")
                    pwm_motor.duty_u16(0)
                    await asyncio.sleep_ms(5)
        else:
            await asyncio.sleep_ms(5)

async def hold():
    while True:
        await asyncio.sleep(60)

async def main():
    hold0 = asyncio.create_task(hold())
    motor0 = asyncio.create_task(motor())
    await asyncio.sleep_ms(5)
    pb = Pushbutton(button)
    pb.press_func(push)
    print("READY!\n")
    await hold0

asyncio.run(main())

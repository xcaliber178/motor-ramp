print("\nInitializing...\n")
from machine import Pin
from machine import PWM
from time import sleep
from primitives import Pushbutton
import uasyncio as asyncio

pwm_motor = PWM(Pin(13))
button = Pin(18, Pin.IN, Pin.PULL_DOWN)
b_high = Pin(19, Pin.OUT)

pwm_motor.freq(20000)
pwm_motor.duty_u16(0)
b_high.on()

state = 0
ramping = False
press = False

def push():
    print("\n-----Pushed-----")
    global state
    global ramping
    global press
    
    ramping = True
    press = True
    
    if state == 0:
        state = 1
    elif state == 1:
        state = 0

async def motor():
    global ramping
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
                    duty_start = 0
                
                for duty in range(duty_start, 65535, 65):
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
                    
                for duty in range(duty_start, 0, -65):
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

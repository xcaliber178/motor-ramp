from machine import Pin
from machine import PWM
from machine import Timer
from time import sleep
import uasyncio as asyncio

button = Pin(18, Pin.IN, Pin.PULL_UP)

pwm_motor = PWM(Pin(13))
pwm_motor.freq(15000)

press = False
state = False

async def check_button():
    global press
    while True:
        if button == True:
            press = True
            print("BUTTON")
        await asyncio.sleep_ms(5)

async def current_state():
    global state
    global press
    while True:
        if press == True:
            press = False
            if state == False:
                state = True
                print("ON RAMP")
                for duty in range(0, 1000, 1):
                    print(duty)
                    #pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
            elif state == True:
                state = False
                print("OFF RAMP")
                for duty in range(1000, 0, -1):
                    print(duty)
                    #pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
        else:
            await asyncio.sleep_ms(5)

async def main():
    task0 = asyncio.create_task(check_button())
    task1 = asyncio.create_task(current_state())
    await task0

asyncio.run(main())

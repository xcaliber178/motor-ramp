from machine import Pin
from machine import PWM
from time import sleep
import uasyncio as asyncio

button = Pin(18, Pin.IN, Pin.PULL_DOWN)
b_high = Pin(19, Pin.OUT)
b_high.on()

#pwm_motor = PWM(Pin(13))
#pwm_motor.freq(15000)

press = False
state = False

async def check_button():
    print("check_button() started!")
    global press
    
    while True:
        if button.value() is 1:
            press = True
            print("\n-------BUTTON-------\n")
        await asyncio.sleep_ms(15)


async def current_state():
    print("current_state() started!")
    global state
    global press

    while True:
        if press == True:
            press = False
            print("Changing motor state...")
            if state == False:
                state = True
                print("ON RAMP")

                for duty in range(0, 65535, 65):
                    print(duty)
                    #pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)

                print("FULL ON")
                #pwm_motor.duty_u16(65535)
                await asyncio.sleep_ms(5)

            elif state == True:
                state = False
                print("OFF RAMP")

                for duty in range(65535, 0, -65):
                    print(duty)
                    #pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)

                print("FULL OFF")
                #pwm_motor.duty_u16(0)
                await asyncio.sleep_ms(5)

        else:
            await asyncio.sleep_ms(5)


async def main():
    task0 = asyncio.create_task(check_button())
    task1 = asyncio.create_task(current_state())
    await task0

asyncio.run(main())

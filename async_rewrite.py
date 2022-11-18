from machine import Pin
from machine import PWM
from machine import Timer
from time import sleep
import asyncio

button = Pin(18, Pin.IN, Pin.PULL_UP)

pwm_motor = PWM(Pin(13))
pwm_motor.freq(15000)

'''
debounce_timer = Timer()

state = False
irq0 = False
'''

press = False
state = False

async def check_button():
    global press
    while True:
        if button == True:
            press = True
            await asyncio.sleep_ms(5)

async def current_state():
    global press
    while True:
        if press == True:
            if state == False:
                state = True
            elif state == True:
                state = False
        await asyncio.sleep_ms(5)
#Continue from here
async def turn_on():
    for duty in range(0, 65535, 1):
        print(duty)
        #pwm_motor.duty_u16(duty)
        sleep(0.001)

async def turn_off():
    for duty in range(65535, 0, -1):
        print(duty)
        #pwm_motor.duty_u16(duty)
        sleep(0.001)

async def main():
    asyncio.create_task(check_button())

asyncio.run(main())

'''
def debounce():
    debounce_timer.init(mode=Timer.ONE_SHOT, period=200, callback=press)

def turn_on():
    for duty in range(0, 65535, 1):
        print(duty)
        #pwm_motor.duty_u16(duty)
        sleep(0.001)

def turn_off():
    for duty in range(65535, 0, -1):
        print(duty)
        #pwm_motor.duty_u16(duty)
        sleep(0.001)

def press(debounce_timer):
    global state

    if state == False:
        state = True
        turn_on()

    elif state == True:
        state = False
        turn_off()

def irq_set(pin):
    global irq0
    irq0 = True

button.irq(irq_set, Pin.IRQ_FALLING)

while True:
    if irq0 == True:
        irq0 = False
        debounce()
'''

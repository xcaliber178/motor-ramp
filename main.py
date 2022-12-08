# Jonas Geisel, 2022, MIT License
# Innovative Cloud Technologies

# Implements a ramp up/down period for a motor controller using PWM and a pushbutton.


# CONTROLLER SETTINGS
Button_Pin = 18 #GPIO
Button_HIGH_Pin = 19 #GPIO
PWM_Pin = 13 #GPIO
PWM_Freq = 10000 #Hz
PWM_Start = 5 #%
PWM_Max = 100 #%
Ramp_Up_Time = 20 #sec
Ramp_Down_Time = 20 #sec


# Imports
from machine import Pin
from machine import PWM
from primitives import Pushbutton
import uasyncio as asyncio

# Set PWM pins and settings
pwm_motor = PWM(Pin(PWM_Pin)) # PWM pin
pwm_motor.freq(PWM_Freq) # PWM frequency
pwm_motor.duty_u16(0) # Makes sure PWM is at minimum

# Set button pins
button = Pin(Button_Pin, Pin.IN, Pin.PULL_DOWN) # Sense pin
high = Pin(Button_HIGH_Pin, Pin.OUT) # High pin
high.on() # Enable high pin

# Math to pass settings to PWM controls
PWM_start_val = int((PWM_Start / 100) * 65535) # Converts start percentage to a usable integer
PWM_max_val = int((PWM_Max / 100) * 65535) # Converts start percentage to a usable integer
PWM_int_up = int((PWM_max_val - PWM_start_val) // (Ramp_Up_Time * 100)) # Calculates step size to meet ramp up time
PWM_int_dn = -int((PWM_max_val // (Ramp_Down_Time * 100))) # Calculates step size to meet ramp down time

state = 0 # Stores the motors state
press = False # Temporarily stores a button press

# Settings validation
if PWM_Start < 0 or PWM_Start >= 100:
    raise Exception("PWM_Start is a silly value! You should probably check that.")
if PWM_Max > 100 or PWM_Max <= 0:
    raise Exception("PWM_Max is a silly value! You should probably check that.")
if Ramp_Down_Time <= 0:
    raise Exception("Ramp_Down_Time is a silly value! You should probably check that.")
if Ramp_Up_Time <= 0:
    raise Exception("Ramp_Up_Time is a silly value! You should probably check that.")
if PWM_Start >= PWM_Max:
    raise Exception("PWM_Start and PWM_Max are the same...why would you even do that?")


def push(): # Is called by a button press, reads current motor state and flips it
    print("PRESS\n")
    global state
    global press
    press = True # Stores button press
    
    if state == 0: # OFF -> ON
        state = 1
    elif state == 1: # ON -> OFF
        state = 0


async def motor():
    global press
    exit = False # Stores exit event

    while True:
        if press == True:
            press = False # Resets the button press memory

            if state == 1: # Motor ramp up
                print("STARTING...\n")
                if exit == True: # If the motor was ramping down and the button was pressed, this will start the ramp up from the last duty cycle value
                    duty_start = duty_mem
                    exit = False # Resets the exit event
                elif exit == False:
                    duty_start = PWM_start_val # Passes the controller setting for PWM
                for duty in range(int(duty_start), PWM_max_val, PWM_int_up): # Main ramp up loop
                    if press == True: # Stores duty cycle value if the button is pressed during ramp up
                        duty_mem = duty
                        exit = True # Stores the exit event
                        break
                    print((duty / 65535) * 100) # Converts current duty cycle value to percentage (used for setup/diagnostics)
                    pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
                if exit != True: # Finishes off the ramp up loop by setting the duty cycle to max
                    print("FULL ON\n")
                    pwm_motor.duty_u16(PWM_max_val)
                    await asyncio.sleep_ms(5)

            elif state == 0: # Motor ramp down
                print("STOPPING...\n")
                if exit == True: # If the motor was ramping up and the button was pressed, this will start the ramp down from the last duty cycle value
                    duty_start = duty_mem
                    exit = False # Resets the exit event
                elif exit == False:
                    duty_start = PWM_max_val
                for duty in range(int(duty_start), 0, PWM_int_dn): # Main ramp down loop
                    if press == True: # Stores duty cycle value if the button is pressed during ramp down
                        duty_mem = duty
                        exit = True # Stores the exit event
                        break
                    print((duty / 65535) * 100) # Converts current duty cycle value to percentage (used for setup/diagnostics)
                    pwm_motor.duty_u16(duty)
                    await asyncio.sleep_ms(10)
                if exit != True: # Finishes off the ramp down loop by setting the duty cycle to zero
                    print("FULL OFF\n")
                    pwm_motor.duty_u16(0)
                    await asyncio.sleep_ms(5)

        else:
            await asyncio.sleep_ms(5)


async def hold(): # Non-terminating function
    while True:
        await asyncio.sleep(60)


async def main(): # Asyncio setup
    hold0 = asyncio.create_task(hold()) # Starts non-terminating function
    motor0 = asyncio.create_task(motor()) # Starts primary motor control function
    await asyncio.sleep_ms(5) # Allows the above function time to initialize
    pb = Pushbutton(button) # Creates a pushbutton class from the hardware library
    pb.press_func(push) # Assigns the push() function as the pushbuttons callable
    await hold0 # Non-terminating, keeps program running indefinitely.

asyncio.run(main()) # Run

if False:
    import this

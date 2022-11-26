# motor-ramp
 Implements a ramp up/down period for a motor controller using PWM and a pushbutton.

### Use
 Load `main.py` and `lib/` to MCU
 
 PWM is on **GPIO13** (Pin 17 on RPi Pico)
 
 Button is across **GPIO18** (Pin 24 on Pico) and **GPIO19** (Pin 25 on Pico)
 
 GPIO18 is the sense pin, GPIO19 is HIGH
 
 The minimum value for starting the motor may need adjusted depending on the motor.

 Pins and PWM values are adjustable at the top of the program file.
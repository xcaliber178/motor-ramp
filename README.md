# motor-ramp
 Implements a ramp up/down period for a motor controller using PWM.

### Use
 Load `main.py` and `lib/` to MCU
 
 PWM is on **GPIO13** (Pin 17 on RPi Pico)
 
 Button is across **GPIO18** (Pin 24 on Pico) and **GPIO19** (Pin 25 on Pico)
 
 GPIO18 is the sense pin, GPIO19 is HIGH
 
 Duty cycle starts from 0 and maxes at 65535. The minimum value for starting the motor may need adjusted depending on the motor. Currently this is hard coded and will need to be adjusted as such. Eventually I will make this an easily changable constant.

## System_response.py
***Description-*** A class to model different damping scenarios in a mass-spring-damper system. This class calculates damping coefficients and damping ratios for different damping cases (undamped, critically damped, overdamped, underdamped) and
can be extended to calculate system time responses.

![allresponses](https://github.com/user-attachments/assets/0501b244-390d-4187-8a41-18c9fcf4092d)


## Program1.m
***Description-*** Plots the responses of subjecting a mass-spring-damper system to an initial velocity excitation.

![Matlabresponse](https://github.com/user-attachments/assets/6b92d5fb-2e67-4b16-8e87-c176e3fdb89a)

## Program2.m
***Description-*** plots a free vibration system's displacement, velocity, and acceleration versus time after being subjected to some initial conditions

![3graphresponse](https://github.com/user-attachments/assets/0533ce37-3a32-4c77-a0e3-28fe77c11549)

## Program3.m
***Description-*** For a FORCED vibration of a mass-spring-damper system, we can calculate the amplitude of the forced response given the system parameters m, c, k and the system's overall response equation. The system's response is different than the forced response because the system's response only describes the harmonic motion of the system over time. This script solves for the force amplitude.

![force_and_sys](https://github.com/user-attachments/assets/46f79bc9-7885-4552-b82e-5aa2bdf69cfa)

## quickcopy.py
***Description-***A simple, non-class script for performing the exact same task as system_response.py. I did this to practice programs faster writing faster and simpler


## system_identifier.py

***Description-*** The Holy Grail of Mechanical Vibration Systems. This program is designed to take in any transfer and input function and tell you every characteristic of it(steady state response, error at steady state, percent overshoot, and more).


### Example 1: First Order System

System Analysis:
--------------------------------------------------
Transfer Function: G(s) = (1.00)/(1.00s + 2.00)
Input: u(t) = 4 (step input)
--------------------------------------------------
Time Constant (τ): 0.50 seconds
Steady State Response (yss): 2.00
Steady State Error (ess): 2.00
--------------------------------------------------

### Example 2: Second Order System

System Analysis:
--------------------------------------------------
Transfer Function: G(s) = (25.00)/(1.00s^2 + 4.00s + 25.00)
Input: u(t) = 1 (step input)
--------------------------------------------------
Natural Frequency (ωn): 5.00 rad/s
Damping Ratio (ζ): 0.40
Steady State Response (yss): 1.00
Steady State Error (ess): 0.00
--------------------------------------------------

![Figure_1](https://github.com/user-attachments/assets/171fe5cb-48db-4c1a-bbe2-593f5e42276c)

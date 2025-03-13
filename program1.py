import numpy as np
import matplotlib.pyplot as plt

# System parameters
wn = 5  # Natural frequency (rad/s)
zeta = np.array([0.05, 0.1, 0.2])  # Damping ratios
x0 = 0  # Initial displacement (cm)
v0 = 60  # Initial velocity (cm/s)

# Time vector
t0 = 0
deltat = 0.01  # Time step
tf = 6
t = np.arange(t0, tf + deltat, deltat)  # Ensure inclusive range

# Plot response for each damping ratio
plt.figure()
for z in zeta:
    wd = np.sqrt(1 - z**2) * wn  # Damped natural frequency
    x = np.exp(-z * wn * t) * (((z * x0 + v0) / wd) * np.sin(wd * t) + x0 * np.cos(wd * t))
    plt.plot(t, x, label=f'ζ={z:.2f}')

# Plot formatting
plt.title('Response to Initial Excitation')
plt.xlabel('Time [s]')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.show()

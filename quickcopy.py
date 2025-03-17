import matplotlib.pyplot as plt
import numpy as np

M = 1       # Mass (kg)
K = 1       # Spring constant (N/m)
x_o = 1     # Initial displacement (m)
v = 1       # Initial velocity (m/s)


tarray = []
y1 = []
y2 = []
y3 = []
y4 = []
Z1 = 0 # not damped
Z2 = 1 # Critically damped
Z3 = 3*np.sqrt(K*M) / (2*np.sqrt(K*M)) # over damp, i highly recommend changing the number 3 to some random integer value over 2.
Z4 = np.sqrt(K*M)/(2*np.sqrt(K*M)) #under, this just needs to be between 0 and 1, change it as you wish

wn = np.sqrt(K/M) 

for i in range(99): 
    t = 15 * i / 100 # you can change 15 to whatever you want
    tarray.append(t)
    # in my opinion, this is a really easy way to indexize arrays in python. We are essentially building an array of displacement values for each time step.
    #So, tarray would look like [0, 15*(1/100), 15*(2/100), ..., ] you could alternatively use numpy's "linspace" if you wanted, but i perfer seeing it like this
    #Additionally, y1 would look something like this at the end of the loop : y1 = [ solution for time = 0, solution for  t =15*(1/100), ...]
    y1.append(x_o * np.cos(wn * t) + (v / wn) * np.sin(wn * t))
    y2.append(np.exp(-1 * wn * t) * ((wn * x_o + v) * t + x_o))
    y3.append(np.exp(-Z3 * wn * t) * (
            x_o * np.cosh(wn * np.sqrt(Z3**2 - 1) * t) + 
            (1 / np.sqrt(Z3**2 - 1)) * (Z3 * x_o + v / wn) * np.sinh(wn * np.sqrt(Z3**2 - 1) * t)
        ))
    y4.append(np.exp(-Z4 * wn * t) * (
        x_o * np.cos((wn * np.sqrt(1 - Z4**2)) * t) + 
        (1 / np.sqrt(1 - Z4**2)) * (Z4 * x_o + v / wn) * np.sin((wn * np.sqrt(1 - Z4**2)) * t)
    ))

plt.figure(figsize=(10, 7))
plt.plot(tarray, y1, label='Not Damped (Z1)')
plt.plot(tarray, y2, label='Critically Damped (Z2)')
plt.plot(tarray, y3, label='Over Damped (Z3)')
plt.plot(tarray, y4, label='Under Damped (Z4)')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Displacement vs Time for Different Damping Ratios')
plt.legend()
plt.grid(True)
plt.show()



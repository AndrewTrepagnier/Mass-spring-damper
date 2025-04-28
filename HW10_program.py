import matplotlib.pyplot as plt
import control as ct
import numpy as np
from scipy.signal import residue


# PART 1A =========================================
print("Problemm 1A:")
[R, P, K] = residue([26], [1, 3, 28, 26])
print (P)
#Tells me the roots of the denominator

A_roots = []
A_poles = [-1, -1+5j, -1-5j]
A_gain = [26]

GA_zpk = ct.zpk(A_roots, A_poles, A_gain)
print(f"GS of probelm 1A transfer function is: {GA_zpk}")
plt.figure(1)
ct.pzmap(GA_zpk)
plt.title('Problem 1A Pole-Zero Map')
plt.show()

# PART 1B =========================================
print("Problemm 1B:")
[R, P, K] = residue([104], [1, 6, 34, 104])
print (P)
#Tells me the roots of the denominator

B_roots = []
B_poles = [-4, -1+5j, -1-5j]
B_gain = [104]

GB_zpk = ct.zpk(B_roots, B_poles, B_gain)
print(f"GS of probelm 1B transfer function is: {GB_zpk}")
plt.figure(2)
ct.pzmap(GB_zpk)
plt.title('Problem 1B Pole-Zero Map')
plt.show()

# PART 1C =========================================
print("Problemm 1C:")
[R, P, K] = residue([41], [1, 9, 49, 41])
print (P)
#Tells me the roots of the denominator

C_roots = []
C_poles = [-1, -4+5j, -4-5j]
C_gain = [41]

GC_zpk = ct.zpk(C_roots, C_poles, C_gain)
print(f"GS of probelm 1B transfer function is: {GC_zpk}")
plt.figure(3)
ct.pzmap(GC_zpk)
plt.title('Problem 1C Pole-Zero Map')
plt.show()

#Combined Graph of Step Response
gsa_tf = ct.TransferFunction([26], [1, 3, 28, 26])
gsb_tf = ct.TransferFunction([104], [1, 6, 34, 104])
gsc_tf = ct.TransferFunction([41], [1, 9, 49, 41])
plt.figure(4)
t = np.linspace(0, 10, 1000)  
t1, y1 = ct.step_response(gsa_tf, t)
t2, y2 = ct.step_response(gsb_tf, t)
t3, y3 = ct.step_response(gsc_tf, t)

plt.plot(t1, y1, label='Problem 1A Step Response')
plt.plot(t2, y2, label='Problem 1B Step Response')
plt.plot(t3, y3, label='Problem 1C Step Response')
plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Step Response Comparison')
plt.legend()
plt.show()



# Probelm 2A
A2 = [1]
B2 = [1, 7, 2, 5, 2, 3]
tf_2a= ct.TransferFunction(A2, B2)
plt.figure(5)
ct.pzmap(tf_2a)
plt.title('Poles of Problem 2A')
plt.show()

# Probelm 2B
C2 = [1]
D2 = [1, 7, 2, 5, 2, -3]
tf_2b= ct.TransferFunction(C2, D2)
plt.figure(5)
ct.pzmap(tf_2b)
plt.title('Poles of Problem 2B')
plt.show()

# Probelm 2C
E2 = [1]
F2 = [1, 0, 7, 2, 5, 2, 3]
tf_2c= ct.TransferFunction(E2, F2)
plt.figure(5)
ct.pzmap(tf_2c)
plt.title('Poles of Problem 2C')
plt.show()



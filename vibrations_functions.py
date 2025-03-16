import sympy as sp
import matplotlib.pyplot as plt
from IPython.display import display, Latex
from scipy.integrate import odeint 
import numpy as np

def display_latex(text):
    if isinstance(text, list):
        for thing in text:
            display(Latex(f'${sp.latex(thing)}$'))
    else:
        display(Latex(f'${sp.latex(text)}$'))

#++++++++++++++++++For defining sympy symbols++++++++++++++++++++++
t, s = sp.symbols('t s')


#++++++++++++++++++For defining sympy functions +++++++++++++++++++

I_f, W, V = sp.Function('I_f')(s), sp.Function('W')(s), sp.Function('V')(t)

#+++++++++++++++++For defining an equation+++++++++++++++++++++++++

eq1 = sp.Eq(50*s*W + 10*W, 25*I_f)
print(sp.latex(eq1)) # if you wanted to render to latex
eq2 = sp.Eq(0.001*s*I_f + 5*I_f, V)

#+++++++++++++++solve systems of diff. eqs ++++++++++++++++++++++

solved = sp.solve([eq1, eq2], (W, I_f), dict=True)[0]
# might return something like:
#solved = {W: 25*I_f/(50*s + 10), I_f: some_expression}
solved_list = [sp.Eq(key, value) for key, value in solved.items()]
# converts to [W = 2*I_f, I_f = some_expression]

"""
Solving a system of two equations (eq1 and eq2). The two variables we are solving for are W and I_f., Dict=True tells sympy to solve the 
solution as a dictionary. [0] take the first solution if there are multiple solutions

Take the solution dictionary and convert it into a list of equations. For each variable (key) and its solution(value) , create an equation like variable = solution
"""

#+++++++++++++++calling on a solution in solved array+++++++++++++++
#  this is a characteristic polynomial
poly = 1 / solved[W]*2500*V

"""
solved[W] is the transfer function solution for W(s)
Multiplying by 2500V and taking the reciprocal creates a characteristic polynomial
This polynomial represents the denominator of the transfer function in standard form
The roots of this polynomial determine the system's natural frequencies and stability
"""


#++++++++++++++++Find the Roots++++++++++++++++++++++++++++++++++

roots = list(sp.roots(poly))
print(roots)

"""
This finds values of s where poly = 0
These roots (eigenvalues) describe:
Natural frequencies of the system (imaginary parts)
Decay/growth rates (real parts)
System stability (negative real parts = stable)
"""

# ++++++++++++++++++++++roots of characteristic polynomial can be solved by putting system in to a matrix +++++++++

M = sp.Matrix([
    [50*s + 10, -25], 
    [0, 0.001*s + 5]
])

other_poly = sp.det(M)
print(sp.roots(other_poly))


"""
- The determinant of (sI - A) gives the characteristic polynomial
Where A is the system matrix and I is identity matrix
Both methods (direct polynomial and matrix) should yield equivalent roots
The roots of the characteristic polynomial tell us:
System stability
Natural frequencies
Damping characteristics
System response behavior
This is fundamental to vibration analysis and control system design.

"""
# ++++++++++++++++++++Important Part+++++++++++++++++++++++++++++====================================

m, c, k  =  61.48, 535.8 ,40_000

def diffs(x, _):
    return [
        x[1],
        (1000 - c*x[1] - k*x[0]) / m
    ]
# 1000n steady state force

time = np.linspace(0, 1.4, 1000)
solution = odeint(diffs, [0,0], time)

plt.plot(time, solution[:, 0])
plt.xlabel('Time (s)')
plt.ylabel('$x(t)$ (m)')
plt.minorticks_on()
plt.grid(which='minor', ls=':')
plt.show()


#+++++++++++++++++++++++++++++++++++Problem 3+++++++++++++++++++++++++++++

# Global parameters for the system
M = 1       # Mass (kg)
K = 1       # Spring constant (N/m)
x_o = 1     # Initial displacement (m)
v = 1       # Initial velocity (m/s)

class system_response():
    """
    A class to model different damping scenarios in a mass-spring-damper system.
    
    This class calculates damping coefficients and damping ratios for different
    damping cases (undamped, critically damped, overdamped, underdamped) and
    can be extended to calculate system time responses.
    """
    
    def __init__(self, case=None, C_value=None, Z=None, Sys_time_response=None):
        """
        Initialize the system_response object.
        
        Parameters:
        -----------
        case : str
            The damping case to model ('Not Damped', 'Critically Damped', 
            'Over Damped', or 'Underdamped')
        C_value : float, optional
            Damping coefficient. If None, will be calculated based on the case.
        Z : float, optional
            Damping ratio. If None, will be calculated based on the case.
        Sys_time_response : array-like, optional
            System time response data. Can be populated later.
        """
        self.case = case
        self.C_value = C_value  # Damping coefficient
        self.Z = Z              # Damping ratio (zeta)
        self.Sys_time_response = Sys_time_response 

    def declare_case(self, new_case):
        """
        Set or change the damping case and calculate appropriate C and Z values.
        
        Parameters:
        -----------
        new_case : str
            The damping case to model ('Not Damped', 'Critically Damped', 
            'Over Damped', or 'Underdamped')
        """
        self.case = new_case
        print(f"The case declared is {self.case}, running loop to determine C...")

        if self.case == 'Not Damped':
            # No damping (C=0, Z=0)
            self.C_value = 0
            self.Z = 0

        elif self.case == 'Critically Damped':
            # Critical damping (C=2√(KM), Z=1)
            # System returns to equilibrium without oscillation in minimum time
            self.C_value = 2*np.sqrt(K*M)
            self.Z = 1

        elif self.case == 'Over Damped':
            # Over damping (C>2√(KM), Z>1)
            # System returns to equilibrium without oscillation but slower than critical
            self.C_value = 2*np.sqrt(K*M)
            # For overdamped: C > 2*sqrt(K*M)
            while self.C_value <= 2*np.sqrt(K*M):
                self.C_value += 1
            self.Z = self.C_value / (2*np.sqrt(K*M))

        elif self.case == "Underdamped":
            # Under damping (C<2√(KM), Z<1)
            # System oscillates with decreasing amplitude
            self.C_value = 2*np.sqrt(K*M)
            # For underdamped: C < 2*sqrt(K*M)
            while self.C_value >= 2*np.sqrt(K*M):
                self.C_value -= 1
            self.Z = self.C_value / (2*np.sqrt(K*M))



        print(f"C value: {self.C_value}, Damping ratio: {self.Z}")

critically_damp = system_response()
critically_damp.declare_case("Critically Damped")
import sympy as sp
import matplotlib.pyplot as plt
from IPython.display import display, Latex
from scipy.integrate import odeint 
import numpy as np

# Global parameters for the system
M = 1       # Mass (kg)
K = 1       # Spring constant (N/m)
x_o = 1     # Initial displacement (m)
v = 1       # Initial velocity (m/s)



class system():
    """
    A class to model different damping scenarios in a mass-spring-damper system.
    
    This class calculates damping coefficients and damping ratios for different
    damping cases (undamped, critically damped, overdamped, underdamped) and
    can be extended to calculate system time responses.
    """
    
    def __init__(self, case=None, C_value=None, Z=None, wd=None, Sys_time_response=None):
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
        self.Z = Z  
        self.wn = np.sqrt(K/M) 
        self.wd = wd  # Don't calculate yet, will be set in declare_case
        self.Sys_time_response = Sys_time_response 

    
    def notdamped_response(self, t):
        return x_o*np.cos(self.wn*t) + (v/self.wn)*np.sin(self.wn*t)
    
    def critically_damped_response(self, t):
        return np.exp(-1*self.wn*t)*((self.wn*x_o + v)*t + x_o)
    
    def overdamped_response(self, t):
        return np.exp(-self.Z*self.wn*t) * (
            x_o * np.cosh(self.wn*np.sqrt(self.Z**2 - 1)*t) + 
            (1/np.sqrt(self.Z**2 - 1)) * (self.Z*x_o + v/self.wn) * np.sinh(self.wn*np.sqrt(self.Z**2 - 1)*t)
        )
    def underdamped_response(self, t):
        return np.exp(-self.Z*self.wn*t) * (
        x_o * np.cos(self.wd*t) + 
        (1/np.sqrt(1 - self.Z**2)) * (self.Z*x_o + v/self.wn) * np.sin(self.wd*t)
    )


    def declare_case(self, new_case):
        """Set up system parameters for the given case"""
        self.case = new_case
        print(f"The case declared is {self.case}, running loop to determine C...")

        if self.case == 'Not Damped':
            self.C_value = 0
            self.Z = 0
            self.wd = self.wn*np.sqrt(1 - self.Z**2)  # Fixed this formula
        elif self.case == 'Critically Damped':
            self.C_value = 2*np.sqrt(K*M)
            self.Z = 1
            self.wd = self.wn*np.sqrt(1 - self.Z**2)
        elif self.case == 'Over Damped':
            self.C_value = 2*np.sqrt(K*M)
            # For overdamped: C > 2*sqrt(K*M)
            while self.C_value <= 2*np.sqrt(K*M):
                self.C_value += 1
            self.Z = self.C_value / (2*np.sqrt(K*M))
            self.wd = self.wn*np.sqrt(self.Z**2 - 1)
        elif self.case == "Underdamped":
            self.C_value = 2*np.sqrt(K*M)
            # For underdamped: C < 2*sqrt(K*M)
            while self.C_value >= 2*np.sqrt(K*M):
                self.C_value -= 1
            self.Z = self.C_value / (2*np.sqrt(K*M))
            self.wd = self.wn*np.sqrt(self.Z**2 - 1)

        print(f"C value: {self.C_value}, Damping ratio: {self.Z}")
    
    def calculate_response(self, t):
        """Calculate response based on current case"""
        if self.case == 'Not Damped':
            return self.notdamped_response(t)
        elif self.case == 'Critically Damped':
            return self.critically_damped_response(t)
        elif self.case == 'Over Damped':
            return self.overdamped_response(t)
        elif self.case == 'Underdamped':
            return self.underdamped_response(t)

    def plot_response(self, time_interval, notdamped=False, criticallydamped=False, overdamped=False, underdamped=False):
        """Plot selected responses"""
        time = np.linspace(0, time_interval, time_interval*100)
        
        cases = {
            'Not Damped': notdamped,
            'Critically Damped': criticallydamped,
            'Over Damped': overdamped,
            'Underdamped': underdamped
        }
        
        plt.figure(figsize=(10, 6))
        for case_name, plot_flag in cases.items():
            if plot_flag:
                self.declare_case(case_name)  # Set up parameters
                response = self.calculate_response(time)  # Calculate using time array
                plt.plot(time, response, label=case_name)
        
        plt.title('System Response')
        plt.xlabel('Time (s)')
        plt.ylabel('Displacement')
        plt.grid(True)
        plt.legend()
        plt.show()


# critically_damp = system()
# critically_damp.declare_case("Critically Damped")

# Create an instance of the system
system_instance = system()

# Plot all cases (10 second time interval)
system_instance.plot_response(50, 
                            notdamped=True, 
                            criticallydamped=True, 
                            overdamped=True, 
                            underdamped=True)



from dataclasses import dataclass
from typing import List, Optional, Dict
import numpy as np
import seaborn as sbn
import control as ct
import matplotlib.pyplot as plt

#So far, code is only designed for step input types

@dataclass
class MySystem:
    NumeratorCoe: np.ndarray
    DenominatorCoe: np.ndarray
    order: int = None

    def __post_init__(self):
        assert sum(self.DenominatorCoe) != 0 and max(self.DenominatorCoe) != 0 and min(self.DenominatorCoe) != 0, "Denominator coefficients must be non-zero integers"
        self.determine_order()

    def determine_order(self) -> int:
        if len(self.DenominatorCoe) == 2:
            self.order = 1
        elif len(self.DenominatorCoe) == 3:
            self.order = 2
        else:
            raise ValueError("Not a valid number of coefficients, system must be either first order or second order")

    # def import_system(self) -> tuple[np.ndarray]:
    #     return self.NumeratorCoe, self.DenominatorCoe
    
@dataclass
class InputType:
    input_type: str  # 'step', 'ramp', 'impulse'
    value: float

class ParameterCalculation:
    def __init__(self, numerator_array: np.ndarray, denominator_array: np.ndarray, order: int, input_value: float):
        self.num_coeff = numerator_array
        self.den_coeff = denominator_array
        self.order = order
        self.input = input_value
        self.tau = None
        self.Tp = None
        self.PO = None
        self.Ts_1 = None
        self.Ts_2 = None
        self.Ts_3 = None 
        self.ss_response = None
        self.ss_error = None
        self.wn = None  # Natural frequency
        self.zeta = None  # Damping ratio
        
        # Calculate parameters upon initialization
        self.calculate()
    
    def calculate(self):
        """Calculate system parameters based on order."""
        if self.order == 1:
            self._calculate_first_order()
        elif self.order == 2:
            self._calculate_second_order()
        else:
            raise ValueError("System must be first or second order")
    
    def _calculate_first_order(self):
        """Calculate first order system parameters."""
        # For system G(s) = a/(s + b), τ = 1/b, K = a/b
        self.tau = 1 / self.den_coeff[1]
        K = self.num_coeff[0] / self.den_coeff[1]
        self.ss_response = K * self.input
        #self.ss_error = self.input - self.ss_response
        self.ss_error = self.input*(1-K)
    
    def _calculate_second_order(self):
        """Calculate second order system parameters."""
        # For system G(s) = ω²/(s² + 2ζωs + ω²)
        self.wn = np.sqrt(self.den_coeff[2])  # Natural frequency
        self.zeta = self.den_coeff[1] / (2 * self.wn)  # Damping ratio
        
        # Calculate time domain specifications
        self.Tp = np.pi / (self.wn * np.sqrt(1 - self.zeta**2))  # Peak time
        self.PO = 100 * np.exp(-self.zeta * np.pi / np.sqrt(1 - self.zeta**2))  # Percent overshoot
        
        # Settling times
        self.Ts_0 = 5 / (self.zeta * self.wn)  # 1% settling time
        self.Ts_1 = 4 / (self.zeta * self.wn)  # 2% settling time
        self.Ts_2 = 3 / (self.zeta * self.wn)  # 5% settling time
        self.Ts_3 = 2 / (self.zeta * self.wn)  # 10% settling time
        
        # Steady state calculations
        K = self.num_coeff[0] / self.den_coeff[2]  # DC gain
        self.ss_response = K * self.input
        self.ss_error = self.input*(1-K)
    
    def plot_response(self, show=True):
        """Generate basic time response plot."""
        sys = ct.TransferFunction(self.num_coeff, self.den_coeff)
        t = np.linspace(0, 10, 1000)
        u = np.ones_like(t) * self.input
        _, y = ct.forced_response(sys, t, u)
        
        plt.plot(t, u, 'b-', label='Input: u(t)')
        plt.plot(t, y, 'r--', label='Output: y(t)')
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Amplitude (y)')
        plt.legend()
        if show:
            plt.show()

    def pole_plot(self, show=True):
        """Plot pole-zero map."""
        sys = ct.TransferFunction(self.num_coeff, self.den_coeff)
        ct.pzmap(sys, plot=True, grid=True)
        plt.grid(True)
        if show:
            plt.show()

    def step_plot(self, show=True):
        """Plot step response."""
        sys = ct.TransferFunction(self.num_coeff, self.den_coeff)
        t = np.linspace(0, 3, 1000)
        t, y = ct.step_response(sys, t)
        plt.plot(t, y)
        plt.grid(True)
        if show:
            plt.show()

    def print_parameters(self):
        """Print system parameters."""
        print("\nSystem Parameters:")
        if self.order == 1:
            print(f"Time Constant (τ): {self.tau:.2f} sec")
        else:
            print(f"Natural Frequency (ωn): {self.wn:.2f} rad/s")
            print(f"Damping Ratio (ζ): {self.zeta:.2f}")
            print(f"Peak Time (Tp): {self.Tp:.2f} sec")
            print(f"Percent Overshoot: {self.PO:.1f}%")
            print(f"Settling Times:")
            print(f"  1%: {self.Ts_0:.2f} sec")
            print(f"  2%: {self.Ts_1:.2f} sec")
            print(f"  5%: {self.Ts_2:.2f} sec")
            print(f" 10%: {self.Ts_3:.2f} sec")
        print(f"Steady State Response: {self.ss_response:.2f}")
        print(f"Steady State Error: {self.ss_error:.2f}")





def analyze_transfer_function(numerator_coeffs: list, denominator_coeffs: list, input_amplitude: float = 1.0, t_final: float = 10):
    """
    Analyze a transfer function with given numerator and denominator coefficients.
    
    Args:
        numerator_coeffs (list): Coefficients of numerator in descending order of s
            Example: [1] for 1
                    [2, 1] for 2s + 1
        denominator_coeffs (list): Coefficients of denominator in descending order of s
            Example: [1, 2] for s + 2
                    [1, 2, 1] for s² + 2s + 1
        input_amplitude (float): Amplitude of the step input
        t_final (float): Final time for simulation
    """


    # Convert lists to numpy arrays
    num = np.array(numerator_coeffs)
    den = np.array(denominator_coeffs)
    
    # Create system
    system = MySystem(num, den)
    
    # Calculate and print parameters
    params = ParameterCalculation(num, den, system.order, input_amplitude)
    params.calculate()
    
    print("\nSystem Analysis:")
    print("-" * 50)
    print(f"Transfer Function: G(s) = {format_transfer_function(num, den)}")
    print(f"Input: u(t) = {input_amplitude} (step input)")
    print("-" * 50)
    
    if system.order == 1:
        print(f"Time Constant (τ): {params.tau:.2f} seconds")
    else: # second order
        print(f"Natural Frequency (ωn): {params.wn:.2f} rad/s")
        print(f"Damping Ratio (ζ): {params.zeta:.2f}")
    
    print(f"Steady State Response (yss): {params.ss_response:.2f}")
    print(f"Steady State Error (ess): {params.ss_error:.2f}")
    print("-" * 50)
    params.print_parameters()
    print("-" * 50)
    


    # Plot response
    params.plot_response(t_final)
    params.pole_plot()




def format_transfer_function(num: np.ndarray, den: np.ndarray) -> str:
    """Format transfer function coefficients into a readable string."""
    def format_polynomial(coeffs: np.ndarray, var: str = 's') -> str:
        terms = []
        for i, coef in enumerate(coeffs):
            power = len(coeffs) - i - 1
            if coef == 0:
                continue
            if power == 0:
                terms.append(f"{coef:.2f}")
            elif power == 1:
                terms.append(f"{coef:.2f}{var}")
            else:
                terms.append(f"{coef:.2f}{var}^{power}")
        return " + ".join(terms) if terms else "0"
    
    num_str = format_polynomial(num)
    den_str = format_polynomial(den)
    
    return f"({num_str})/({den_str})"





# Example usage
if __name__ == "__main__":
    # Problem 1: G(s) = 1/(s+2)
    print("\nProblem 1: First Order System")
    analyze_transfer_function([1], [1, 2], input_amplitude=4)
    print("-"*50)
    
    # Problem 2: 
    print("\nProblem 2: Second Order System")
    analyze_transfer_function([49], [1, 7.392, 49], input_amplitude=10)
    print("-"*50)
    """---------------------------------------------------------------------------------------- Part A """
    # Problem 4a - Different damping ratios
    print("\nProblem 4a - Different damping ratios:")
    
    # Create systems
    sys1 = ParameterCalculation(np.array([100]), np.array([1, 4, 100]), 2, 1)  # ζ = 0.2
    sys2 = ParameterCalculation(np.array([100]), np.array([1, 8, 100]), 2, 1)  # ζ = 0.4
    sys3 = ParameterCalculation(np.array([100]), np.array([1, 12, 100]), 2, 1) # ζ = 0.6
    
    # Plot poles
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4a: Pole Locations for Different Damping Ratios")
    sys1.pole_plot(show=False)
    sys2.pole_plot(show=False)
    sys3.pole_plot(show=False)
    plt.legend(['Pole ζ = 0.2', 'Pole ζ = 0.4', 'Pole ζ = 0.6'])
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.show()
    
    # Plot step responses
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4a: Step Responses for Different Damping Ratios")
    sys1.step_plot(show=False)
    sys2.step_plot(show=False)
    sys3.step_plot(show=False)
    plt.legend(['Step Response(ζ = 0.2)', 'Step Response(ζ = 0.4)', 'Step Response(ζ = 0.6)'])
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.show()
    
    # # Plot system responses
    # plt.figure(figsize=(10, 6))
    # plt.title("Problem 4a: System Responses for Different Damping Ratios")
    # sys1.plot_response(show=False)
    # sys2.plot_response(show=False)
    # sys3.plot_response(show=False)
    # plt.legend(['ζ = 0.2', 'ζ = 0.4', 'ζ = 0.6'])
    # plt.show()
    
    # Print parameters for each system
    print("\nParameters for ζ = 0.2:")
    sys1.print_parameters()
    print("\nParameters for ζ = 0.4:")
    sys2.print_parameters()
    print("\nParameters for ζ = 0.6:")
    sys3.print_parameters()

    print("Discussion:\n As Zeta increases and Wn remains constant, the settling times and percent overshoots decrease. Alternatively, peak time increases during this. ")
    
    """---------------------------------------------------------------------------------------- Part B"""
    # Problem 4b - Different natural frequencies (constant zeta)
    print("\nProblem 4b - Different natural frequencies (ζ = 0.3):")
    
    # Create systems with constant zeta = 0.3
    sys1 = ParameterCalculation(np.array([100]), np.array([1, 6, 100]), 2, 1)     # ωn = 10
    sys2 = ParameterCalculation(np.array([400]), np.array([1, 12, 400]), 2, 1)    # ωn = 20
    sys3 = ParameterCalculation(np.array([900]), np.array([1, 18, 900]), 2, 1)    # ωn = 30
    
    # Plot poles
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4b: Pole Locations for Different Natural Frequencies (ζ = 0.3)")
    sys1.pole_plot(show=False)
    sys2.pole_plot(show=False)
    sys3.pole_plot(show=False)
    plt.legend(['Pole ωn = 10', 'Pole ωn = 20', 'Pole ωn = 30'])
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.show()
    
    # Plot step responses
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4b: Step Responses for Different Natural Frequencies (ζ = 0.3)")
    sys1.step_plot(show=False)
    sys2.step_plot(show=False)
    sys3.step_plot(show=False)
    plt.legend(['Step Response(ωn = 10)', 'Step Response(ωn = 20)', 'Step Response(ωn = 30)'])
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.show()
    
    # Print parameters for each system
    print("\nParameters for ωn = 10:")
    sys1.print_parameters()
    print("\nParameters for ωn = 20:")
    sys2.print_parameters()
    print("\nParameters for ωn = 30:")
    sys3.print_parameters()

    print("Discussion:\n As Natural Frequency increases and Zeta remains constant at 0.3, the settling times and peak times decrease. The percent overshoot remains constant since it only depends on Zeta.")
    
    """---------------------------------------------------------------------------------------- Part C"""
    # Problem 4c - Different ζωn values with constant ωd
    print("\nProblem 4c - Different ζωn values (ωd = 40):")
    
    # For ωd = 40, we need to calculate ωn and ζ for each ζωn value
    # Using ωd = ωn√(1-ζ²) = 40 and ζωn = {10, 20, 30}
    
    # For ζωn = 10: solve ωd = ωn√(1-(10/ωn)²) = 40
    # For ζωn = 20: solve ωd = ωn√(1-(20/ωn)²) = 40
    # For ζωn = 30: solve ωd = ωn√(1-(30/ωn)²) = 40
    
    # Calculated values:
    # ζωn = 10: ωn ≈ 41.23, ζ ≈ 0.243
    # ζωn = 20: ωn ≈ 44.72, ζ ≈ 0.447
    # ζωn = 30: ωn ≈ 50.00, ζ ≈ 0.600
    
    sys1 = ParameterCalculation(np.array([1700]), np.array([1, 20, 1700]), 2, 1)    # ζωn = 10
    sys2 = ParameterCalculation(np.array([2000]), np.array([1, 40, 2000]), 2, 1)    # ζωn = 20
    sys3 = ParameterCalculation(np.array([2500]), np.array([1, 60, 2500]), 2, 1)    # ζωn = 30
    
    # Plot poles
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4c: Pole Locations for Different ζωn Values (ωd = 40)")
    sys1.pole_plot(show=False)
    sys2.pole_plot(show=False)
    sys3.pole_plot(show=False)
    plt.legend(['Pole ζωn = 10', 'Pole ζωn = 20', 'Pole ζωn = 30'])
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.show()
    
    # Plot step responses
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4c: Step Responses for Different ζωn Values (ωd = 40)")
    sys1.step_plot(show=False)
    sys2.step_plot(show=False)
    sys3.step_plot(show=False)
    plt.legend(['Step Response(ζωn = 10)', 'Step Response(ζωn = 20)', 'Step Response(ζωn = 30)'])
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.show()
    
    # Print parameters for each system
    print("\nParameters for Zwn = 10:")
    sys1.print_parameters()
    print("\nParameters for Zwn = 20:")
    sys2.print_parameters()
    print("\nParameters for Zwn = 30:")
    sys3.print_parameters()

    print("Discussion:\n As Zwn increases with constant wd, both the settling time and percent overshoot decrease due to increased damping. The peak time increases as the system becomes more damped.")
    
    """---------------------------------------------------------------------------------------- Part D"""
    # Problem 4d - Different ωd values with constant ζωn
    print("\nProblem 4d - Different ωd values (Zwn = 10):")
    
    # For ζωn = 10 constant, we calculate systems for ωd = {20, 30, 40}
    # Using ωd = ωn√(1-ζ²) and ζωn = 10
    
    # Calculated values for ωd = 20, 30, 40:
    # ωd = 20: ωn ≈ 22.36, ζ ≈ 0.447
    # ωd = 30: ωn ≈ 31.62, ζ ≈ 0.316
    # ωd = 40: ωn ≈ 41.23, ζ ≈ 0.243
    
    sys1 = ParameterCalculation(np.array([500]), np.array([1, 20, 500]), 2, 1)     # ωd = 20
    sys2 = ParameterCalculation(np.array([1000]), np.array([1, 20, 1000]), 2, 1)   # ωd = 30
    sys3 = ParameterCalculation(np.array([1700]), np.array([1, 20, 1700]), 2, 1)   # ωd = 40
    
    # Plot poles
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4d: Pole Locations for Different wd Values (Zwn = 10)")
    sys1.pole_plot(show=False)
    sys2.pole_plot(show=False)
    sys3.pole_plot(show=False)
    plt.legend(['Pole wd = 20', 'Pole wd = 30', 'Pole wd = 40'])
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.show()
    
    # Plot step responses
    plt.figure(figsize=(10, 6))
    plt.title("Problem 4d: Step Responses for Different wd Values (Zwn = 10)")
    sys1.step_plot(show=False)
    sys2.step_plot(show=False)
    sys3.step_plot(show=False)
    plt.legend(['Step Response(wd = 20)', 'Step Response(wd = 30)', 'Step Response(wd = 40)'])
    plt.xlabel('Time (sec)')
    plt.ylabel('Amplitude')
    plt.show()
    
    # Print parameters for each system
    print("\nParameters for wd = 20:")
    sys1.print_parameters()
    print("\nParameters for wd = 30:")
    sys2.print_parameters()
    print("\nParameters for wd = 40:")
    sys3.print_parameters()

    print("Discussion:\n As wd increases with constant Zwn, the settling time decreases and the system responds faster. The percent overshoot increases slightly as the damping ratio effectively decreases relative to the natural frequency.")
    
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
    



    def plot_response(self, t_final=10):
        """Generate basic time response plot."""
        sys = ct.TransferFunction(self.num_coeff, self.den_coeff)
        t = np.linspace(0, t_final, 1000)
        u = np.ones_like(t) * self.input
        _, y = ct.forced_response(sys, t, u)
        
        plt.figure(figsize=(10, 6))
        plt.plot(t, u, 'b-', label='Input')
        plt.plot(t, y, 'r--', label='Output')
        plt.grid(True)
        plt.xlabel('Time (sec)')
        plt.ylabel('Amplitude')
        plt.legend()
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
    else:  # second order
        print(f"Natural Frequency (ωn): {params.wn:.2f} rad/s")
        print(f"Damping Ratio (ζ): {params.zeta:.2f}")
    
    print(f"Steady State Response (yss): {params.ss_response:.2f}")
    print(f"Steady State Error (ess): {params.ss_error:.2f}")
    print("-" * 50)
    params.print_parameters()
    print("-" * 50)
    
    # Plot response
    params.plot_response(t_final)

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
    # Example 1: G(s) = 1/(s+2)
    print("\nExample 1: First Order System")
    analyze_transfer_function([1], [1, 2], input_amplitude=4)
    
    # Example 2: G(s) = 25/(s² + 4s + 25)
    print("\nExample 2: Second Order System")
    analyze_transfer_function([25], [1, 4, 25], input_amplitude=1)

    # Example 3: G(s) = 400/(2s² + 4s + 100)
    print("\nExample 3(Problem 2): Second Order System")
    analyze_transfer_function([400], [2, 4, 100], input_amplitude=2)
    
    # You can easily analyze any other transfer function by calling:
    # analyze_transfer_function([num_coeffs], [den_coeffs], input_amplitude)
    
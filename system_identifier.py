from dataclasses import dataclass
from typing import List, Optional, Dict
import numpy as np
import seaborn as sbn
import control as ct

#So far, code is only designed for step input types

@dataclass
class MySystem:
    NumeratorCoe : np.ndarray
    DenominatorCoe  : np.ndarray
    order : int = None

    def __post_init__(self):
       assert sum(self.DenominatorCoe) != 0 and max(self.DenominatorCoe) != 0 and min(self.DenominatorCoe) != 0,  "Denominator coefficients must be non-zero intergers" # if it evalueates to true it does nothing, makes sure there will not be a zero in denominator

    def determine_order(self) -> int:
        if len(self.DenominatorCoe) == 2:
            self.order = 1
        elif len(self.DenominatorCoe) == 3:
            self.order = 2
        else:
            print("Not a valid number of coefficients, system must be either first order or second order")

    # def import_system(self) -> tuple[np.ndarray]:
    #     return self.NumeratorCoe, self.DenominatorCoe
    
@dataclass
class input_type:
    input : str
    value : float


class parameter_calculation:
    def __init__(self, numerator_array, denominator_array, order, input_value):
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

    def calculate(self):

        # Parameter Calculations for a first order system
        if self.order == 1: 

            self.tau = 1/self.num_coeff.index[0] #Calculate Time Constant
                






    
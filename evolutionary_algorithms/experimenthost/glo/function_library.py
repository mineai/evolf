#import numpy as np
import random



class FunctionLibrary:

    """
    
    This class contains the library of possible operators that we can
    retrieve as input for the nodes of the trees. 

    *For the time being, I am unable to properly import numpy so I put
    string representations of the Unary operators as a temporary fix
    to test the rest of the function library.

    """

    FUNCTIONS = {
        # "U": [
        #     np.cos,
        #     np.sin,
        #     np.log,
        #     np.exp,
        #     np.mean
        # ],

        "U": [
            "cos",
            "sin",
            "log",
            "exp",
            "mean"
        ],
        "B": [
            "+",
            "-",
            "*",
            "/"
        ],
        "L": [
            "x",
            "y",
            1,
            -1
        ]
    }

    def sample(self, operator_type):
        assert operator_type.upper() in self.FUNCTIONS.keys(), "Function not available"
        functions_available = self.FUNCTIONS.get(operator_type)
        sampled_function = functions_available[random.randint(0,len(functions_available)-1)]

        return {
            operator_type.upper(): sampled_function
        }

    def get_required_literals(self):
        return {
            "L": self.FUNCTIONS["L"][:2]
        }

    def get_available_coefficients(self):
        return {
            "L": self.FUNCTIONS["L"][1:]
        }
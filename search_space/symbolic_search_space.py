

class SymbolicSearchSpace:
    full_search_space = {}

    import sympy as sp
    import numpy as np

    # This gives the range of possible symbolic functions usable
    symbolic_search_space = {
            "cos": sp.cos,
            "sin": sp.sin,
            "log": sp.log,
            "exp": sp.exp,
            "tan": sp.tan,
            "square": np.square,
            "sqrt": lambda x: np.power(x, 0.5),
            "cosh": sp.cosh,
            "sinh": sp.sinh,
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "y": sp.Symbol("y_pred"),
            "t": sp.Symbol("y_true"),
            "pos_scalar": 1,
            "neg_scalar": -1,
            "mean": np.mean,
            "sum": np.sum,
            "max": np.max,
            "min": np.min,
            "acosh": sp.acosh,
            "asinh": sp.asinh
    }

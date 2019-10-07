import sympy as sp


class Validate:

    @staticmethod
    def validate_literal_existance(symbolic_expression):
        y_pred_deriv = sp.diff(symbolic_expression,
                               sp.Symbol("y_pred"))
        y_true_deriv = sp.diff(symbolic_expression,
                               sp.Symbol("y_true"))

        if y_pred_deriv != 0 and y_true_deriv != 0:
            return True
        else:
            return False

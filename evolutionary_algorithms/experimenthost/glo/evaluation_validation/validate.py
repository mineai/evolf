import sympy as sp


class Validate:
    """
    This class contains all the methods required
    to validate if the given Sympy expresion is valid
    for GLO Tree or not.
    """
    @staticmethod
    def has_required_literals(symbolic_expression, literals):
        """
        This functions uses differentials to validate
        if the given symbolic expression have all the required
        literals or not.
        :param symbolic_expression: The sympy Expression to be checked
        :param literals: A List containing literals of type str.
        :return boolean value: That informs if the expression has all
        the required literals or not
        """
        for literal in literals:
            deriv = sp.diff(symbolic_expression,
                            sp.Symbol(literal))
            if deriv == 0:
                return False

        return True

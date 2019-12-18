

class ArgumentParser:
    """
    This class serves as interface
    for the argument parser.
    The functions in this class are the base
    functions that any argument parser should
    inherit and overwrite.
    """

    def add_parser(self):
        """""
        This function adds the argument parser
        to take in inputs from the CLI
        """""
        raise NotImplementedError


    def absorb_args(self):
        """""
        This function extracts the necessary parameters 
        from the supplied args.
        """""
        raise NotImplementedError
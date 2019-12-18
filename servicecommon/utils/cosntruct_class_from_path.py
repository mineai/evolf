

class ConstructClassFromPath:
    """
    This class is used to construct
    classes from package paths,
    """

    @staticmethod
    def construct(class_path, class_name):
        """
        Thus function takes in a module path
        in xx.xx.xx.ABC format and returns
        a class Object.
        :param path:
        :return:
        """
        # Get the Components individually
        components = class_path.split('/')
        module_path = ".".join(components)
        module = __import__(module_path, fromlist=['my_class'])
        klass = getattr(module, class_name)

        return klass

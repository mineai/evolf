import json

class JsonPersistor():

    def __init__(self, base_file_name=".", folder=""):
        """
        This constructor initializes the name of the file to
        persist at what path.

        :param base_file_name: Name of the file without the .json
        extension
        :param folder: Location of the file to persist
        :returns nothing
        """
        self.base_file_name = base_file_name
        self.folder = folder

    def persist(self, dict):
        """
        This function takes in a dictionary and
        persists at the path with the base_file_name
        :param dict: Dictornary to persist
        :returns nothing
        """
        if not self.base_file_name:
            file_name = "default_dict"
        else:
            file_name = self.base_file_name
        if not self.folder[-1] == "/":
            self.folder += "/"
        with open(self.folder + self.base_file_name +'.json', 'w') as fp:
            json.dump(dict, fp, indent=4)

    def restore(self):
        """
        This function loads a json from the
        base_file_name in the specified folder
        in a dictionary format.
        :params none
        :returns dict: Dictionary created from the
        JSON
        """
        if not self.folder[-1] == "/":
            self.folder += "/"
        file = self.folder + self.base_file_name +'.json'
        try:
            dict = json.load(file)
        except e:
            print(e)

        return dict

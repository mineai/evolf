from evolf.servicecommon.persistor.local.pickle.pickle_persistor import PicklePersistor


class SurrogateDataPersistor:
    """
    class variables:
        - linearized_tree: A list containing the nodes from a tree in level order.

        - search_space_dictionary: A dictionary that contains a key named "search_space"

        - search_space_operators: A list of all operators from the search space dictionary
        excluding root (R) operator types.

        - fitness: Holds the fitness passed in on object creation so the fitness can be
        easily attributed to the resulting image.

    methods:
        - persist(): Persists the image and fitness passed in by either adding it to the
        existing pickle file or creating a new pickle file

        - restore(): Loads the value of the pickle file into a variable and returns it

        - set_operators(): Extrapolates all of the search space operators from the
        dictionary and puts them in the list defined as search_space_operators

        - get_image(): returns a matrix of 1's and 0's that represents the tree with
        respect to the defined search space.

        - get_image_row(index): returns a list containing 0's corresponding to operators
        that the node doesn't contain and a 1 corresponding to the operator that it does
    """

    def __init__(self, linearized_tree, search_space_dictionary, fitness, persistence_folder,
                 persistence_name='surrogate_data'):
        self.linearized_tree = linearized_tree
        self.search_space_dictionary = search_space_dictionary
        self.fitness = fitness
        self.persistence_folder = persistence_folder
        self.persistence_name = persistence_name
        self.search_space_operators = []

    def persist(self):

        """

        If there is an existing pickle file,

            - load the contents into a temporary dictionary using the restore() method
            from PicklePersistor
            - add the fitness and tree image to it.
            - persist the pickle file to the desired path

        If the pickle file hasn't been created yet,

            - create a dictionary with the following structure
                {
                    "image":[image1, image2, image3, ..., imageN],
                    "fitness":[fitness1, fitness2, fitness3, ..., fitnessN]
                }
            - add the fitness and tree image to it
            - persist the pickle file to the desired path

        :return: None
        """

        import os

        # check to see if the pickle exists
        if os.path.exists(self.persistence_folder + self.persistence_name):
            # if it does, load the data off of it and append the new information

            # load the pickle file onto a temporary_variable
            restored_pickle = self.restore()

            # delete the old pickle file
            os.remove(self.persistence_folder + self.persistence_name)

            # append the new image and fitness
            restored_pickle['image'].append(self.get_image())
            restored_pickle['fitness'].append(self.fitness)

            # persist the updated dictionary
            PicklePersistor(self.persistence_name, self.persistence_folder).persist(restored_pickle)

        else:
            # if it does not exist, create the dictionary and persist it

            image_dictionary = {"image": [self.get_image()], "fitness": [self.fitness]}

            PicklePersistor(self.persistence_name, self.persistence_folder).persist(image_dictionary)

    def restore(self):
        """

        Using the restore() method from PicklePersistor, return the loaded contents of the pickle file

        :return: restored_pickle
        """

        return PicklePersistor(self.persistence_name, self.persistence_folder).restore()

    def set_operators(self):
        """

        Extrapolates all of the search space operators from the dictionary and
        puts them in the list defined as search_space_operators

        :return: None
        """

        all_operators = []
        ss_dictionary = self.search_space_dictionary.get("search_space")
        operator_types = ss_dictionary.keys()

        for key in operator_types:
            if key not in ['R']:
                operators = ss_dictionary.get(key).keys()
                for operator in operators:
                    all_operators.append(operator)

        self.search_space_operators = all_operators

    def get_image(self):
        """

        returns a matrix of 1's and 0's that represents the tree with respect
        to the defined search space.

        :return: tree
        """

        tree_image = []

        self.set_operators()

        for node in self.linearized_tree:
            if node in self.search_space_operators:
                tree_image.append(self.get_image_row(self.search_space_operators.index(node)))

        # (pickled_tree) = pickle.dump(tree_image, open(path+"surrogate_data.p", "wb"))

        return tree_image

    def get_image_row(self, index):

        """

        returns a list containing 0's corresponding to operators that the node
        doesn't contain and a 1 corresponding to the operator that it does

        :param index:
        :return: row: array of 0's and a 1
        """

        row = []
        length = len(self.search_space_operators)

        for i in range(0, length):
            if i == index:
                row.append(1)
            else:
                row.append(0)

        return row

class TreeUtils:

    # Returns the contents of a tree in the preorder sequence
    @classmethod
    def preorder_print(cls, start, traversal=''):
        # Root -> Left -> Right
        if start:
            traversal += (str(start.function_str) + ' ')
            traversal = cls.preorder_print(start.left, traversal)
            traversal = cls.preorder_print(start.right, traversal)
        return traversal

    # Returns the contents of a tree in the inorder sequence
    @classmethod
    def inorder_print(cls, start, traversal=''):
        # Left -> Root -> Right
        if start:
            traversal = cls.inorder_print(start.left, traversal)
            traversal += (str(start.function_str) + ' ')
            traversal = cls.inorder_print(start.right, traversal)
        return traversal

    # Returns the contents of a tree in the postorder sequence
    @classmethod
    def postorder_print(cls, start, traversal=''):
        # Left -> Right -> Root
        if start:
            traversal = cls.preorder_print(start.left, traversal)
            traversal = cls.preorder_print(start.right, traversal)
            traversal += (str(start.function_str) + ' ')
        return traversal

    @staticmethod
    def traverse_tree(tree, evaluation_type="inorder", reverse=True):
        if evaluation_type.lower() == "postorder":
            func_str = TreeUtils().postorder_print(tree.root)
        elif evaluation_type.lower() == "preorder":
            func_str = TreeUtils().preorder_print(tree.root)
        elif evaluation_type.lower() == "inorder":
            func_str = TreeUtils().inorder_print(tree.root)

        if reverse:
            func = func_str.split(" ")[::-1]
        else:
            func = func_str.split(" ")
        func.remove('')
        return func

    @staticmethod
    def sort_trees_by_fitness_desc(tree_list):
        import copy
        tree_list = copy.copy(tree_list)
        import numpy as np
        sorted_trees = []
        fitness = []

        [fitness.append(tree.fitness) for tree in tree_list]
        while len(tree_list):
            best_tree = tree_list[np.argmax(fitness)]
            sorted_trees.append(best_tree)
            tree_list.remove(best_tree)
            fitness.remove(max(fitness))

        return sorted_trees





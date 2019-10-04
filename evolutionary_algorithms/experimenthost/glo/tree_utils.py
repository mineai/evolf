class TreeUtils:

    # Returns the contents of a tree in the preorder sequence
    @classmethod
    def preorder_print(cls, start, traversal=[]):
        # Root -> Left -> Right
        if start:
            traversal += (str(start.data) + ' ')
            traversal = cls.preorder_print(start.left, traversal)
            traversal = cls.preorder_print(start.right, traversal)
        return traversal
    
    # Returns the contents of a tree in the inorder sequence
    @classmethod
    def inorder_print(cls, start, traversal=''):
        # Left -> Root -> Right
        if start:
            traversal = cls.inorder_print(start.left, traversal)
            traversal += (str(start.data) + ' ')
            traversal = cls.inorder_print(start.right, traversal)
        return traversal
    
    # Returns the contents of a tree in the postorder sequence
    @classmethod
    def postorder_print(cls, start, traversal=''):
        # Left -> Right -> Root
        if start:
            traversal = cls.preorder_print(start.left, traversal)
            traversal = cls.preorder_print(start.right, traversal)
            traversal += (str(start.data) + ' ')
        return traversal
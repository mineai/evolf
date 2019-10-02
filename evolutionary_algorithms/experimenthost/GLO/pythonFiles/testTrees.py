class Node(object):
    
    # Constructor function
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    
class BinaryTree(object):

    # Constructor function
    def __init__(self, root):
        self.root = Node(root)

    def _init(self, root):
        

    # Prints the tree out in any desired order
    def print_tree(self, traversal_type):
        if traversal_type == 'preorder':
            return self.preorder_print(self.root, '')
        elif traversal_type == 'inorder':
            return self.inorder_print(self.root, '')
        elif traversal_type == 'postorder':
            return self.postorder_print(self.root, '')
        else:
            print('Traversal type ',traversal_type,' not available')
    
    # Returns the contents of a tree in the preorder sequence
    def preorder_print(self, start, traversal):
        # Root -> Left -> Right
        if start:
            traversal += (str(start.value) + '-')
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
        return traversal
    
    # Returns the contents of a tree in the inorder sequence
    def inorder_print(self, start, traversal):
        # Left -> Root -> Right
        if start:
            traversal = self.inorder_print(start.left, traversal)
            traversal += (str(start.value) + '-')
            traversal = self.inorder_print(start.right, traversal)
        return traversal
    
    # Returns the contents of a tree in the postorder sequence
    def postorder_print(self, start, traversal):
        # Left -> Right -> Root
        if start:
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
            traversal += (str(start.value) + '-')
        return traversal

# Crude method of populating a tree
def crudePopulate():    
    tree = BinaryTree(1)
    tree.root.left = Node(2)
    tree.root.right = Node(3)
    tree.root.left.left = Node(4)
    tree.root.left.right = Node(5)
    tree.root.right.left = Node(6)
    tree.root.right.right = Node(7)

    return tree

# Prints out the contents of the tree in various orders
def print_tree_all(tree):
    print('Preorder: ',tree.print_tree('preorder'))
    print('Inorder: ',tree.print_tree('inorder'))
    print('Postorder: ',tree.print_tree('postorder'))
    

    
def run():
    try:
        tree = crudePopulate()
        print('Tree Successfully Populated!')
    except:
        print('Something went wrong with populating the tree.')

    try:
        print_tree_all(tree)
    except:
        print('Something went wrong with printing the tree.')
run()
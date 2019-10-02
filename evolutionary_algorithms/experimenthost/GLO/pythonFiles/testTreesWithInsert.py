class Node:
    # Constructor
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None

class BST:
    # Constructor
    def __init__(self):
        self.root = None
    
    def insert(self, data):
        # if the root is empty, populate it with data
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(data, self.root)
    
    def _insert(self, data, cur_node):
        # if data is less than the current node,
        # go to its left child
        if data < cur_node.data:

            # if the left child is empty          
            if cur_node.left is None:
                
                # put the data there              
                cur_node.left = Node(data)
            
            # if there is something there  
            else:

                # call the _insert function again with the 
                # left child set as the current node to see
                # where the data should be placed
                self._insert(data, cur_node.left)

        # if data is greater than the current node,
        # go to its right child
        elif data > cur_node.data:

            # if the right child is empty
            if cur_node.right is None:

                # put the data there
                cur_node.right = Node(data)

            # if there is something there
            else:

                # call the _insert function again with the 
                # right child set as the current node to see
                # where the data should be placed
                self._insert(data, cur_node.right)
        else:
            print('Value is already present in tree.')

    def find(self, data):
        if self.root:
            is_found = self._find(data, self.root)
            if is_found:
                return True
            return False
        else:
            return None
        
    def _find(self, data, cur_node):
        if data > cur_node.data and cur_node.right:
            return self._find(data, cur_node.right)
        elif data < cur_node.data and cur_node.left:
            return self._find(data, cur_node.left)
        if data == cur_node.data:
            return True


def populateBST():
    bst = BST()

    bst.insert(4)
    bst.insert(2)
    bst.insert(8)
    bst.insert(5)
    bst.insert(10)

    return bst

def run():
    bst = populateBST()

    print(bst.find(1))

run()

            

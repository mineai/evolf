import random
import pydot
from pptree import *
import timeit
chars = ['U','B','L']

class Node:
    # Constructor
    def __init__(self, type=None, data=None):
        self.data = data
        self.type = type
        self.left = None
        self.right = None

class Tree:
    # Constructor
    def __init__(self, min_height=3, max_height=10):
        self.height = 0
        self.root = None
        self.max_height = max_height
        self.min_height = max_height
        self.unary_count = 0
        self.binary_count = 0
        self.literal_count = 0


    # returns a token based on the instantanious 
    # height of the tree taking into account the
    # min and max heights set earlier

    def reqTok(self):
        if self.height < self.min_height:
            # return 'U' | 'B' 
            return chars[random.randint(0,1)]
        elif self.height >= self.max_height:            
            # return L
            return 'L'
        else:
            # return 'U' | 'B' | 'L'   
            return chars[random.randint(0,2)]

    # returns a Node that corresponds to the tok that
    # was passed in

    def helperFunct(self, tok):
        if tok == 'U':
            return self.Unary(tok)
        elif tok == 'B':
            return self.Binary(tok)
        elif tok == 'L':
            return self.Literal(tok)
        return None
    
    # A literal Node will not have any children

    def Literal(self, tok):
        myNode = Node(tok)
        self.literal_count += 1
        myNode.right = None
        myNode.left = None
        return myNode

    # A binary Node will have two children, each of
    # which are going to be randomly selected using
    # reqTok() and helperFunct()

    def Binary(self, tok):
        myNode = Node(tok)
        # Increments the tree height
        self.height += 1
        self.binary_count += 1
        myNode.left = self.helperFunct(self.reqTok()) 
        myNode.right = self.helperFunct(self.reqTok())
        return myNode

    # A unary Node will have one child that will be
    # randomly selected using reqTok() and helperFunct()

    def Unary(self, tok):
        myNode = Node(tok)
        # Increments the tree height
        self.height += 1
        self.unary_count += 1
        myNode.left = self.helperFunct(self.reqTok())  
        myNode.right = None     
        return myNode

    # Prints out the contents of a tree

    def print_tree(self, current_node, level=0):
        if current_node:
            num_tabs = '\t'*(self.height - level)
            ret = num_tabs+repr(current_node.type)+'\n'
            ret += self.print_tree(current_node.right, level)
            level += 1
            ret += self.print_tree(current_node.left, level)
            level +=1
            return ret
        return ''

    def traverse(self, rootnode):
        thislevel = [rootnode]
        a = '                                                                 '
        #a = self.height
        while thislevel:
            nextlevel = list()
            a = a[:len(a)-3]
            for n in thislevel:
                print a+str(n.type),
                if n.left: 
                    nextlevel.append(n.left)
                if n.right: 
                    nextlevel.append(n.right)
                print
                thislevel = nextlevel

def generateTreeList(size):
    myTrees = []

    while(len(myTrees) < size):
        myTrees.append(Tree())

    for tree in myTrees:
        tok = tree.reqTok()
        tree.root = tree.helperFunct(tok)

    return myTrees

def printTreeList(treeList):
    index = 1
    badTreeCount = 0
    for tree in treeList:
        print('Tree #'+str(index))
        print('Tree Height: '+str(tree.height))
        print('# of U\'s: '+str(tree.unary_count))
        print('# of B\'s: '+str(tree.binary_count))
        print('# of L\'s: '+str(tree.literal_count))
        if tree.binary_count < 1:
            print('Bad Tree! Not enough Binary operators.')
            badTreeCount += 1
        elif tree.literal_count < 2:
            print('Bad Tree! Not enough Literals.')
            badTreeCount += 1
        print(tree.print_tree(tree.root))
        index += 1
    print(str(badTreeCount)+' out of '+str(len(treeList))+' trees were bad.')
    

    
def run():
    #start = timeit.timeit() 
    treeList = generateTreeList(100)
    printTreeList(treeList)
    #end = timeit.timeit()
    #print('Executed in '+str(end-start)+'s.')

run()

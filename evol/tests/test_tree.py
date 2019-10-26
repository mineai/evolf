import random
import os

from evol.elements.tree.tree import Tree

tree = Tree(4, 4)

random_node = random.choice(tree.nodes)
while random_node.node_id == 1:
    random_node = random.choice(tree.nodes)

random_node.coefficient = 4

tree.reset_tree()

path = f"{os.getcwd()}/results/glo_test_add_tree/0"
tree.visualize_tree(path)

# print("Expression before Mutation: ", tree.symbolic_expression)
#
# node_to_add_to = random.choice(tree.nodes)
# while node_to_add_to.operator_type in ["R"]:
#     node_to_add_to = random.choice(tree.nodes)
#
# operator_type = "B"
# function_str = "*"
# symbolic_handle = FunctionLibrary.get_symbolic_handle(function_str)
# tensorflow_handle = FunctionLibrary.get_tensorflow_handle(function_str)
# multiplicative_parent = Node(operator_type=operator_type, function_str=function_str,
#      symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)
#
# weight = random.uniform(1, 10)
# operator_type = "L"
# function_str = "pos_scalar"
# symbolic_handle = weight*FunctionLibrary.get_symbolic_handle(function_str)
# tensorflow_handle = weight*FunctionLibrary.get_tensorflow_handle(function_str)
# another_child = Node(operator_type=operator_type, function_str=function_str,
#      symbolic_handle=symbolic_handle, tensorflow_handle=tensorflow_handle)
#
# tree.insert_binary_parent(node_to_add_to, multiplicative_parent, another_child)
# tree.reset_tree()
# print("Expression After Mutation: ", tree.symbolic_expression)
# path = f"{os.getcwd()}/results/glo_test_add_tree/1"
# tree.visualize_tree(path)
#

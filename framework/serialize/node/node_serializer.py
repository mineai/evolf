from framework.elements.node.node import Node
from framework.elements.node.node_constructor import NodeConstructor
from framework.interfaces.serialize.serialize import Serialize


class NodeSerializer(Serialize):
    """
    This class inherits from the Base Framework class
    Serialize and overrides the serialize and deserialize
    methods to serialize the Node class as dictionary.
    """
    def __init__(self, node_objs=None, search_space_obj=None):
        """
        :param node_objs: A list containing objects of Node class
        or a dictionary containing the serialized node objects
        that have to be restored
        :param search_space_obj: Object of Search Space classe
        """
        self.node_objs = node_objs if isinstance(node_objs, list) \
                                      or isinstance(node_objs, dict) \
            else [node_objs]
        self.search_space_obj = search_space_obj

    def serialize(self):
        """
        This function loops over the available params of the node
        class and adds them as key:value pairs to a dictionary.
        1) Non serializable parameters like function handles are deleted
        as they can be restored from the 'function_str' param of Node class.
        2) Params pointing to other node objects like 'left', 'right', etc
        are replaced by the object's class member 'node_id'
        :return nodes: A dictionary containing the serialized node/nodes
        """
        nodes = {}
        for node_obj in self.node_objs:
            assert isinstance(node_obj, Node), "Expected Object to be of type Node"
            node_dictionary = node_obj.__dict__
            node_dictionary["left"] = node_obj.left.node_id if node_obj.left is not None else None
            node_dictionary["right"] = node_obj.right.node_id if node_obj.right is not None else None
            node_dictionary["parent"] = node_obj.parent.node_id if node_obj.parent is not None else None
            del node_dictionary["symbolic_handle"]
            del node_dictionary["tensorflow_handle"]

            nodes[node_obj.node_id] = node_dictionary

        return nodes

    def get_node_by_id(self, id, nodes):
        """
        This function returns the desired node_id
        from a list of given node objects
        :param id: The node_id to be queried
        :param nodes: A list containing node objects
        :return desired_node: Node Object with the desired 'id'
        """
        desired_node = [node for node in nodes if node.node_id == id][0]
        return desired_node

    def assign_parents_and_children(self, nodes):
        """
        This function loops over node objects constructed
        after deserializing nodes and assigns children or parent
        from the nodes list as based on their node_id.
        :param nodes: A list containing node objects
        :return nodes: Nodes
        """
        for node in nodes:
            node.left = self.get_node_by_id(node.left, nodes) if node.left is not None else None
            node.right = self.get_node_by_id(node.right, nodes) if node.right is not None else None
            node.parent = self.get_node_by_id(node.parent, nodes) if node.parent is not None else None

        return nodes

    def deserialize(self):
        """
        This function deserializes a serialized dictionary consisting of nodes in the
        format:
        {node_id : {
            function_str: 'log',
            node_id: 1,
            ...
            }
            .
            .
            .
        }
        :return nodes: A list containing all the node objects deserialized.
        """
        assert isinstance(self.node_objs, dict), "Expected A Dictionary of Nodes"
        nodes = []
        for node_id in self.node_objs.keys():
            node_info = self.node_objs.get(node_id)
            node_type = node_info.get("operator_type")
            node_function = node_info.get("function_str")
            left_child = node_info.get("left")
            right_child = node_info.get("right")
            parent = node_info.get("parent")

            if node_type == "U":
                node = NodeConstructor.create_unary_node(operator=node_function,
                                                         search_space_obj=self.search_space_obj)
            elif node_type == "B":
                node = NodeConstructor.create_binary_node(operator=node_function,
                                                          search_space_obj=self.search_space_obj)
            elif node_type == "L":
                node = NodeConstructor.create_literal_node(operator=node_function,
                                                           search_space_obj=self.search_space_obj)
            elif node_type == "R":
                node = NodeConstructor.create_root_node(operator=node_function,
                                                        search_space_obj=self.search_space_obj)
            else:
                raise ValueError("Node Type Not Known")
            node.node_id = node_id
            node.left = left_child
            node.right = right_child
            node.parent = parent

            nodes.append(node)

        nodes = self.assign_parents_and_children(nodes)
        return nodes

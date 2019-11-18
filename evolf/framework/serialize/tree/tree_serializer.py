from evolf.framework.elements.tree.tree import Tree
from evolf.framework.serialize.node.node_serializer import NodeSerializer
from evolf.framework.interfaces.serialize.serialize import Serialize


class TreeSerializer(Serialize):

    def __init__(self, tree_objs=None, search_space_obj=None):
        """
        :param tree_objs: A list containing objects of Tree class
        or a dictionary containing the serialized Tree objects
        that have to be restored
        :param search_space_obj: Object of Search Space class
        """
        self.tree_objs = tree_objs if isinstance(tree_objs, list) \
                                      or isinstance(tree_objs, dict) \
            else [tree_objs]
        self.search_space_obj = search_space_obj

    def serialize(self):
        """
        This function loops over the available params of the Tree
        class and adds them as key:value pairs to a dictionary.
        1) Non serializable parameters like function handles are deleted
        2) The essential node param of the Tree class is serialized using NodeSerializer
        and serialized as a dict
        :return nodes: A dictionary containing the serialized tree/trees
        """
        import json
        trees = []
        for tree in self.tree_objs:
            assert isinstance(tree, Tree), "Expected object to be of type Tree"
            tree_dict = tree.__dict__
            tree = {}
            for tree_param in tree_dict.keys():
                param_val = tree_dict[tree_param]

                if tree_param == 'nodes':
                    node_serializer = NodeSerializer(param_val)
                    serialized_nodes = node_serializer.serialize()
                    tree[tree_param] = serialized_nodes
                else:
                    try:
                        json.dumps(param_val)
                        tree[tree_param] = param_val
                    except Exception as e:
                        continue

            trees.append(tree)

        trees = trees[0] if len(trees) == 1 else trees

        return trees

    def deserialize(self):
        """
        This function deserializes a serialized dictionary consisting of a tree or a list
        of trees in the
        format:
        [   {
            "fitness": x,
            "avg_epoch_time": y,
            "nodes": {
                node_id : {
                        function_str: 'log',
                        node_id: 1,
                        ...
                        }
                        .
                        .
                        .
                }
            },
            {
            .
            .
            .
            },
            .
            .
            .
        ]
        :return deserialized_trees: A list containing all the Tree objects deserialized.
        """
        assert isinstance(self.tree_objs, list) and isinstance(self.tree_objs[0], dict), "Expected A List of " \
                                                                                         "Serialized Trees "
        deserialized_trees = []
        for serialized_tree in self.tree_objs:
            fitness = serialized_tree.get("fitness", 0)
            avg_epoch_time = serialized_tree.get("avg_epoch_time", None)
            nodes = serialized_tree.get("nodes")

            node_deserializer = NodeSerializer(node_objs=nodes,
                                               search_space_obj=self.search_space_obj)
            deserialized_nodes = node_deserializer.deserialize()

            tree_args = {
                "fitness": fitness,
                "avg_epoch_time": avg_epoch_time,
                "nodes": deserialized_nodes
            }

            tree = Tree(None, None,
                        self.search_space_obj,
                        tree_args)
            deserialized_trees.append(tree)

        return deserialized_trees

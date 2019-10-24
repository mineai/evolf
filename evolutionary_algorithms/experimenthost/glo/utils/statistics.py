
class Statistics:
    """
    This class contains functions to compute statistics of a tree object
    """
    @staticmethod
    def statistics(tree):
        """
        Thus function takes a tree and returns a dict
        containing several params about the tree.
        :param tree: Object of tree type
        :return stats: A dict containing several statistics about the tree
        """
        stats = {
            "height": tree.height,
            "U": tree.unary_count,
            "B": tree.binary_count,
            "L": tree.literal_count,
            "expression": str(tree.symbolic_expression),
            "fitness": tree.fitness,
            "avg_epoch_time": tree.avg_epoch_time
        }

        return stats

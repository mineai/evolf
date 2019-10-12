
class Statistics:

    @staticmethod
    def statistics(tree):
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

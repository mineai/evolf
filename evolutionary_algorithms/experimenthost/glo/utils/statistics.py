
class Statistics:

    @staticmethod
    def statistics(tree):
        stats = {
            "height": tree.height,
            "U": tree.unary_count,
            "B": tree.binary_count,
            "L": tree.literal_count
        }

        return stats

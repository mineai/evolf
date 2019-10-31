from neat.genotype.genome import Genome
import random

class Crossover:
    """
    This class handles the crossover described in the
    original NEAT paper.
    """

    @staticmethod
    def crossover(parent_1, parent_2, fitness):

        # Create a Gene
        child = Genome()

        # Ensure Parent 1 is the more fit
        # parent
        if fitness[0] < fitness[1]:
            parent_1, parent_2 = parent_2, parent_1

        # Get the parent_1 nodes as a list of NodeGene objects
        parent_1_nodes = list(parent_1.get_nodes().values())

        # Crossover the NODEGENE
        # Loop over the the parent_1_nodes and add them to the child
        # as a clone of the object
        for node in parent_1_nodes:
            child.add_node(node.clone_gene())

        # Crossover the CONNECTIONGENE
        for innovation_number, innovation in parent_1.get_connection_genes().items():
            if innovation_number in list(parent_2.get_connection_genes()):
                # Matching Gene - Chose randomly from either parent
                random_parent = [parent_1, parent_2][random.randint(0, 1)]
                child.add_connection_gene(random_parent.get_connection_genes()[innovation_number].clone_gene())
            else:
                # Disjoint or Excess Gene -
                if fitness[0] == fitness[1]:
                    # Randomly Sampled if equal fitness
                    random_parent = [parent_1, parent_2][random.randint(0, 1)]
                    if innovation_number in random_parent.get_connection_genes().keys():
                        child_con_gene = random_parent.get_connection_genes()[innovation_number].clone_gene()
                    else:
                        continue
                else:
                    # Inherited from the fit parent
                    child_con_gene = innovation.clone_gene()
                child.add_connection_gene(child_con_gene)

        return child


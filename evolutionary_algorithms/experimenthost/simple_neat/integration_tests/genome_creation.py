from evolutionary_algorithms.experimenthost.simple_neat.genotype.connection_gene import ConnectionGene
from evolutionary_algorithms.experimenthost.simple_neat.genotype.genome import Genome
from evolutionary_algorithms.experimenthost.simple_neat.genotype.node_gene import NodeGene
from evolutionary_algorithms.experimenthost.simple_neat.network_constructor.network_constructor import \
    NetworkConstructor
from evolutionary_algorithms.experimenthost.simple_neat.reporduction.crossover.crossover import Crossover
from evolutionary_algorithms.experimenthost.simple_neat.reporduction.mutation.mutation import Mutation
from evolutionary_algorithms.experimenthost.simple_neat.visualize.visualize import Visualize

import os
import time
import calendar
from tqdm import trange
import random

class GenomeCreationTest():
    """
    This is a class that tests the creation and mutation
    of a specific Genome
    """

    @staticmethod
    def initialize(num_inputs, num_outputs):
        """
        This Function uses the NEAT Genome to construct a network
        """
        genome = Genome()
        nodes, connection_genes, next_innovation = NetworkConstructor().construct_network(num_inputs, num_outputs,
                                                                                          # "fully_connected"
                                                                                          )
        genome.set_nodes_from_list(nodes)
        genome.set_connection_genes_from_list(connection_genes)
        mutation_obj = Mutation(next_innovation)
        return genome, mutation_obj


def test_sample_creation(base_dir, method):
    genome = Genome()

    if method == 1:
        genome.add_node(NodeGene("INPUT", 1))
        genome.add_node(NodeGene("INPUT", 2))
        genome.add_node(NodeGene("INPUT", 3))
        genome.add_node(NodeGene("OUTPUT", 4))
        genome.add_node(NodeGene("HIDDEN", 5))

        genome.add_connection_gene(ConnectionGene(1, 4, random.uniform(-1, 1), True, 1))
        genome.add_connection_gene(ConnectionGene(2, 4, random.uniform(-1, 1), False, 2))
        genome.add_connection_gene(ConnectionGene(3, 4, random.uniform(-1, 1), True, 3))
        genome.add_connection_gene(ConnectionGene(2, 5, random.uniform(-1, 1), True, 4))
        genome.add_connection_gene(ConnectionGene(5, 4, random.uniform(-1, 1), True, 5))
        genome.add_connection_gene(ConnectionGene(1, 5, random.uniform(-1, 1), True, 8))

    elif method == 2:
        genome.add_node(NodeGene("INPUT", 1))
        genome.add_node(NodeGene("INPUT", 2))
        genome.add_node(NodeGene("INPUT", 3))
        genome.add_node(NodeGene("OUTPUT", 4))
        genome.add_node(NodeGene("HIDDEN", 5))
        genome.add_node(NodeGene("HIDDEN", 6))

        genome.add_connection_gene(ConnectionGene(1, 4, random.uniform(-1, 1), True, 1))
        genome.add_connection_gene(ConnectionGene(2, 4, random.uniform(-1, 1), False, 2))
        genome.add_connection_gene(ConnectionGene(3, 4, random.uniform(-1, 1), True, 3))
        genome.add_connection_gene(ConnectionGene(2, 5, random.uniform(-1, 1), True, 4))
        genome.add_connection_gene(ConnectionGene(5, 4, random.uniform(-1, 1), False, 5))
        genome.add_connection_gene(ConnectionGene(5, 6, random.uniform(-1, 1), True, 6))
        genome.add_connection_gene(ConnectionGene(6, 4, random.uniform(-1, 1), True, 7))
        genome.add_connection_gene(ConnectionGene(3, 5, random.uniform(-1, 1), True, 9))
        genome.add_connection_gene(ConnectionGene(1, 6, random.uniform(-1, 1), True, 10))

    return genome

def crossover_test(base_dir):
    genome_1 = test_sample_creation(base_dir, 1)
    genome_2 = test_sample_creation(base_dir, 2)
    Visualize.visualize(genome_1, f"{base_dir}/genome_1")
    Visualize.visualize(genome_2, f"{base_dir}/genome_2")

    child = Crossover().crossover(genome_1, genome_2, [4, 4])
    mutation_obj = Mutation(11)
    Visualize.visualize(child, f"{base_dir}/child")

    return child, mutation_obj



def test_create_genome_automatic(base_dir):
    # Construct and Mutate for N generations.
    num_inputs = 5
    num_outputs = 1
    test_obj = GenomeCreationTest()

    genome_obj, mutation_obj = test_obj.initialize(num_inputs,
                                                   num_outputs)

    Visualize.visualize(genome_obj, f"{base_dir}/initial_candidate")

    return genome_obj, mutation_obj


def test_mutate(genome_obj, mutation_obj, num_times):
    num_iterations = num_times
    for _ in trange(1, num_iterations + 1):
        # base_gen_dir = f"{base_dir}/gen{iteration_num}"
        # os.makedirs(base_gen_dir)
        node_objs = list(genome_obj.get_nodes().values())
        connection_objs = list(genome_obj.get_connection_genes().values())
        genome_obj.set_connection_genes_from_list(mutation_obj.mutate_connections(node_objs,
                                                                                  connection_objs))
        # Visualize().visualize(genome_obj, f"{base_gen_dir}/mutated_weight")
        node_objs = list(genome_obj.get_nodes().values())
        connection_objs = list(genome_obj.get_connection_genes().values())
        nodes, connections = mutation_obj.mutate_node(node_objs, connection_objs)
        genome_obj.set_nodes_from_list(nodes)
        genome_obj.set_connection_genes_from_list(connections)
        # Visualize().visualize(genome_obj, f"{base_gen_dir}/mutated_node")

    Visualize().visualize(genome_obj, f"{base_dir}/final_mutated_candidate")


experiment_id = calendar.timegm(time.gmtime())

print(f"To refer to this test Experiment, the ID is: {experiment_id}")

base_dir = f"{os.getcwd()}/results/neat_integration_test_{experiment_id}"

os.makedirs(base_dir)

# gemome_obj, mutation_obj = test_create_genome(base_dir)
# test_mutate(gemome_obj, mutation_obj, 20)

child, mutation_obj = crossover_test(base_dir)
test_mutate(child, mutation_obj, 10)
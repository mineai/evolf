from tqdm import trange


class Visualize():

    @staticmethod
    def visualize(genome_obj, name):
        print(f"Visualizing {name}")
        import pydot
        graph = pydot.Dot(graph_type='digraph',
                          label=f"Candidate {name}",
                          fontsize=16,
                          fontname='Roboto',
                          rankdir="LR",
                          ranksep=1)
        input_graph = pydot.Subgraph(ontsize=16,
                                     fontname='Roboto',
                                     rankdir="LR",
                                     rank="same")
        output_graph = pydot.Subgraph(ontsize=16,
                                      fontname='Roboto',
                                      rankdir="LR",
                                      rank="same")

        colors = {
            "INPUT": "#F5A286",
            "HIDDEN": "#A8CFE7",
            "OUTPUT": "#F7D7A8"
        }

        node_dict = {}
        nodes = list(genome_obj.get_nodes().values())
        for node_idx in trange(len(nodes)):
            node = nodes[node_idx]
            node_type = node.get_type().name
            node_color = colors[node_type]
            node_obj = pydot.Node(node.get_id(),
                                  label=f"{node.get_id()}",
                                  xlabel="",
                                  xlp=5,
                                  orientation=0,
                                  height=1,
                                  width=1,
                                  fontsize=10,
                                  shape='circle',
                                  style='rounded, filled',
                                  color=node_color,
                                  fontcolor="white")

            node_dict[node.get_id()] = node_obj
            if node_type == "INPUT":
                input_graph.add_node(node_obj)
            elif node_type == "OUTPUT":
                output_graph.add_node(node_obj)
            else:
                graph.add_node(node_obj)

        width = 2
        connections = list(genome_obj.get_connection_genes().values())
        for connection_idx in trange(len(connections)):
            connection = connections[connection_idx]
            if connection.is_expressed():
                weight = connection.get_weight()
                if weight >= 0:
                    color = "#AADFA2"
                else:
                    color = "red"
            else:
                pass
                # color = "grey"
                color = "white"
            src = node_dict[connection.get_in_node()]
            dst = node_dict[connection.get_out_node()]

            edge = pydot.Edge(src, dst,
                              color=color,
                              label=f"{connection.get_innovation_number()}, {connection.get_weight()}",
                              fontcolor="#979ba1",
                              fontsize=10)
            graph.add_edge(edge)

        graph.add_subgraph(input_graph)
        graph.add_subgraph(output_graph)

        graph.write_png(f"{name}.png")

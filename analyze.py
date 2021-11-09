import networkx as nx
import vk
import tqdm


def construct_two_graphs(G, edge_list, node_list):
    with_hidden = G
    
    return with_hidden, without_hidden

def get_main_info(G, graph_name):
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])
    d = dict(G.degree)
    print(d.items())
    avg_degree = sum([item[1] for item in d.items()])/len(G.nodes())
    res = ""
    res += "Number of nodes: " + str(len(G.nodes())) + '\n'
    res += "Number of edges: " + str(len(G.edges())) + '\n'
    res += "Average path length: " + str(nx.average_shortest_path_length(G0)) + '\n'
    res += "Average clustering: " + str(nx.average_clustering(G0)) + '\n'
    res += "Average degree: " + str(avg_degree) + '\n'
    res += "Diameter: " + str(nx.diameter(G0)) + '\n'
    res += "Radius: " + str(nx.radius(G0))
    print("Stats for graph " + graph_name + ": ")
    print(res)
    print("Saving to " + graph_name + ".txt")
    with open(graph_name + ".txt", "w") as f:
        f.write(res)




def full_analysis(G):
    return 0
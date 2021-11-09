import networkx as nx
import vk
import tqdm
import numpy as np

def construct_two_graphs(G, edge_list, node_list):
    with_hidden = G
    without_hidden = nx.Graph()
    for node in G.nodes():
        if node not in node_list:
            without_hidden.add_node(node)
    for edge in G.edges():
        if edge not in edge_list:
            without_hidden.add_edge(edge[0], edge[1])
    delete_single_nodes = []
    for node in without_hidden.nodes():
        if without_hidden.degree[node] == 0:
            delete_single_nodes.append(node)
    for node in delete_single_nodes:
        without_hidden.remove_node(node)
    Gcc = sorted(nx.connected_components(without_hidden), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])
    print("With hidden connected: ", nx.is_connected(with_hidden))
    print("Without hidden connected: ", nx.is_connected(G0))
    return with_hidden, G0

def get_main_info(G, graph_name, wo_hid=False):
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    G0 = G.subgraph(Gcc[0])
    d = dict(G.degree)
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
    name = graph_name + "/"+ graph_name + ".txt"
    if wo_hid:
        name = graph_name + "/without_hidden_"+ graph_name + ".txt"
    with open(name, "w") as f:
        f.write(res)


def eig_laplacian(G):
    D = [[0 for i in G.nodes()] for j in G.nodes()]
    node_translation = {}
    j = 0
    for i in G.nodes():
        node_translation.update({i : j})
        j += 1
    for i in G.nodes():
        D[node_translation[i]][node_translation[i]] = G.degree[i]
    D = np.array(D)
    A = nx.adjacency_matrix(G).todense()
    L = D - A
    v, u = np.linalg.eigh(L)
    res = []
    for row in u:
        res.append(row.tolist()[0])
    return np.array(res), v

def spectral_two_clusters(vecs):
    sec_vec  = vecs[:, 1]
    res = []
    for i in range(sec_vec.shape[0]):
        if sec_vec[i] < 0:
            res.append(0)
        else:
            res.append(1)
    return res

def lambda_clusterization(G):
    vecs, vals = eig_laplacian(G)
    clustering = spectral_two_clusters(vecs)
    return clustering

def full_analysis(G):
    return 0
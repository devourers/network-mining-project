import networkx as nx

def merge_graphs(G1, G2):
    G = G1
    for node in G2.nodes():
        if node not in G.nodes():
            G.add_node(node)
    for edge in G2.edges():
        if edge not in G.edges():
            G.add_edge(edge[0], edge[1])
    return G
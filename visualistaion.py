import networkx as nx
import matplotlib.pyplot as plt

def form_kawada_kawai(G):
    print("Forming kamada-kawai layout...")
    pos1 = nx.kamada_kawai_layout(G)
    print("Formed kawada-kawai layout.")
    return pos1

def draw_both_graphs(G, hidden_friends, edge_list, user1_id, user2_id):
    d = dict(G.degree)
    plt.figure(figsize=(32, 18), dpi=60)
    pos1 = form_kawada_kawai(G)
    other_edges = [edge for edge in G.edges() if edge not in edge_list]
    other_nodes = [node for node in G.nodes() if node not in hidden_friends]
    spec_node_size = [d[user1_id] * 10, d[user2_id] * 10]
    hidden_node_sizes = [5*d[v] for v in hidden_friends]
    normal_node_sizes = [5*d[v] for v in other_nodes]
    nx.draw_networkx_nodes(G, pos1, nodelist=other_nodes, node_size=normal_node_sizes, node_color="tab:blue")
    nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
    nx.draw_networkx_edges(G, pos1, edgelist=other_edges)
    plt.savefig("without_hidden.png", format = "PNG")
    #second graph -- with hidden friends
    nx.draw_networkx_nodes(G, pos1, nodelist=hidden_friends, node_size=hidden_node_sizes, node_color="yellow")
    nx.draw_networkx_edges(G, pos1, edgelist=edge_list, edge_color='tab:red')
    plt.savefig("with_hidden.png", format = "PNG")
    plt.close()
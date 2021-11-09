import networkx as nx
import matplotlib.pyplot as plt
import analyze

def form_kawada_kawai(G):
    print("Forming kamada-kawai layout...")
    pos1 = nx.kamada_kawai_layout(G)
    print("Formed kawada-kawai layout.")
    return pos1

def draw_both_graphs(G, hidden_friends, edge_list, user1_id, user2_id, pos1, graph_name):
    d = dict(G.degree)
    plt.figure(figsize=(32, 18), dpi=60)
    
    other_edges = [edge for edge in G.edges() if edge not in edge_list]
    other_nodes = [node for node in G.nodes() if node not in hidden_friends]
    spec_node_size = [d[user1_id] * 10, d[user2_id] * 10]
    hidden_node_sizes = [5*d[v] for v in hidden_friends]
    normal_node_sizes = [5*d[v] for v in other_nodes]
    nx.draw_networkx_nodes(G, pos1, nodelist=other_nodes, node_size=normal_node_sizes, node_color="tab:blue")
    nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
    nx.draw_networkx_edges(G, pos1, edgelist=other_edges)
    plt.savefig(graph_name + "/"+ graph_name + "_without_hidden.png", format = "PNG")
    #second graph -- with hidden friends
    nx.draw_networkx_nodes(G, pos1, nodelist=hidden_friends, node_size=hidden_node_sizes, node_color="yellow")
    nx.draw_networkx_edges(G, pos1, edgelist=edge_list, edge_color='tab:red')
    plt.savefig(graph_name + "/"+ graph_name + "_with_hidden.png", format = "PNG")
    plt.close()

def visualise_clustering(G, graph_name, graph, pos1, user1_id, user2_id, wo_hid=False):
    clustering_with = analyze.lambda_clusterization(graph)
    plt.figure(figsize=(32, 18), dpi=60)
    d = dict(G.degree)
    #with_hidden
    spec_node_size = [d[user1_id] * 10, d[user2_id] * 10]
    
    graph_dict = {}
    node_list_with = list(G.nodes())
    j = 0
    for i in G.nodes():
        if i in graph.nodes():
            if clustering_with[j] == 1:
                graph_dict.update({i : 1})
            else:
                graph_dict.update({i : 0})
            j += 1
    graph_node_sizes_1 = [5*d[v] for v in graph.nodes() if graph_dict[v] == 1]
    graph_node_sizes_0 = [5*d[v] for v in graph.nodes() if graph_dict[v] == 0]
    nx.draw_networkx_nodes(G, pos1, nodelist=[node for node in graph_dict if graph_dict[node] == 1], \
    node_size=graph_node_sizes_1, node_color="violet")
    nx.draw_networkx_nodes(G, pos1, nodelist=[node for node in graph_dict if graph_dict[node] == 0], \
    node_size=graph_node_sizes_0, node_color="orange")
    nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
    nx.draw_networkx_edges(G, pos1, edgelist=graph.edges())
    name = graph_name + "/"+ graph_name + "_lambda_without_hidden.png"
    if wo_hid == True:
        name = graph_name + "/with_hidden_"+ graph_name + "_lambda_without_hidden.png"
    plt.savefig(name, format = "PNG")
    plt.close()
import networkx as nx
import matplotlib.pyplot as plt
import analyze
import numpy as np
import os

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
    #spec_node_size = [d[user1_id] * 10, d[user2_id] * 10]
    hidden_node_sizes = [5*d[v] for v in hidden_friends]
    normal_node_sizes = [5*d[v] for v in other_nodes]
    nx.draw_networkx_nodes(G, pos1, nodelist=other_nodes, node_size=normal_node_sizes, node_color="tab:blue")
    #nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
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
    #spec_node_size = [d[user1_id] * 10, d[user2_id] * 10]
    
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
    #nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
    nx.draw_networkx_edges(G, pos1, edgelist=graph.edges())
    name = graph_name + "/"+ graph_name + "_lambda_without_hidden.png"
    if wo_hid == True:
        name = graph_name + "/with_hidden_"+ graph_name + "_lambda_without_hidden.png"
    plt.savefig(name, format = "PNG")
    plt.close()

def visualise_netstalking_coeficients(res, coefs):
    fig, ax = plt.subplots()
    ax.set_title("Netstalking coefficient", fontsize=20)
    plt.ylabel("Coefficient \n [0, 1]", fontsize=15)
    plt.xlabel("Sample sizes", fontsize=15)
    ax.set_ylim(0, 1.01)
    ax.set_xticks([])
    ax.set_yticks([i/100 for i in range(0, 101, 5)])
    i = 0
    for r in res:
        plots = np.array(r)
        ax.scatter(plots[0], plots[1])
        curr_annotation = "Friends size " + str(coefs[i][0]) + "\n FoF size " + str(coefs[i][1])
        if i % 2 == 1:
            mult = -1
        else:
            mult = 0
        pos = (plots[0] - 0.01, plots[1] + mult * 0.03)
        ax.annotate(curr_annotation, pos, fontsize=8)
        i += 1
    plt.show()
    
def visualize_cliques(G, pos, size, colors, widths, graph_name):
    print(len(colors))
    try:
        os.makedirs(graph_name + '/Cliques/')
    except:
        pass
    for i in range(colors.shape[0]):
        b_edges = np.array(list(G.edges))[widths[i] == widths[i].max()]
        plt.figure(figsize=(8*2, 8))
        nodes = nx.draw_networkx_nodes(G, pos,node_color=colors[i], node_size=100, linewidths=1, edgecolors='black')
        nx.draw_networkx_edges(G,pos, alpha=0.3, width=widths[i].min())
        nx.draw_networkx_edges(G, pos, width=widths[i].max(), edgelist=b_edges)
        plt.title('Clique of the size {}'.format(size))
        plt.axis('off')
        plt.savefig(graph_name + '/Cliques/clique_' + str(i+1) + ".png")
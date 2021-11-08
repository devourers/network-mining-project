import networkx as nx
import vk
import tqdm

version = "5.81"

def merge_graphs(G1, G2):
    print('Merging graphs...')
    G = G1
    print('Nodes...')
    for node in tqdm.tqdm(G2.nodes()):
        if node not in G.nodes():
            G.add_node(node)
    print('Edges...')
    for edge in tqdm.tqdm(G2.edges()):
        if edge not in G.edges():
            G.add_edge(edge[0], edge[1])
    print('Merged graphs...')
    return G

def finish_graph(G, vk_api):
    print("Checking mutuality...")
    log = ""
    log_num = 0
    for node in tqdm.tqdm(G.nodes()):
        try:
            res = dict(vk_api.friends.get(v=version, user_id=node))['items']
            for node_2 in res:
                if (node, node_2) not in G.edges() and (node_2, node) not in G.edges() and node_2 in G.nodes():
                    G.add_edge(node, node_2)
        except:
            log += "Private data on user " + str(node) + "\n"
            log_num += 1
    print("Finished generating friend graph. Across " + str(len(G.nodes())) +" accounts following " + str(log_num) +" were private")
    print(log)
    print('Mutuality added')
    return G
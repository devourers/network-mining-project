import networkx as nx
import vk
import tqdm
import connection
import friends

version = "5.81"

def merge_graphs(G1, G2, logging = True):
    if logging == False:
        G = G1
        for node in G2.nodes():
            if node not in G.nodes():
                G.add_node(node)
        for edge in G2.edges():
            if edge not in G.edges():
                G.add_edge(edge[0], edge[1])
        return G 
    G = G1
    print('Nodes...')
    for node in tqdm.tqdm(G2.nodes()):
        if node not in G.nodes():
            G.add_node(node)
    print('Edges...')
    for edge in tqdm.tqdm(G2.edges()):
        if edge not in G.edges():
            G.add_edge(edge[0], edge[1])
    print('Merged graphs.')
    return G

def finish_graph(G, vk_api, logging=True):
    if logging==False:
        for node in G.nodes():
            try:
                res = dict(vk_api.friends.get(v=version, user_id=node))['items']
                for node_2 in res:
                    if (node, node_2) not in G.edges() and (node_2, node) not in G.edges() and node_2 in G.nodes():
                        G.add_edge(node, node_2)
            except:
                continue
        return G
    #==========================
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

def construct_graph(user1_id, user2_id, sample_size):

    vk_api = connection.connect()

    user1_G, hid_1, hid_fof_1 = friends.form_graph(user1_id, 1, vk_api, sample_size)
    user2_G, hid_2, hid_fof_2 = friends.form_graph(user2_id, 2, vk_api, sample_size)

    G = merge_graphs(user1_G, user2_G)
    G = finish_graph(G, vk_api)
    both_hidden = []
    for v in hid_1:
        if v in hid_2:
            both_hidden.append(v)
    hidden_friends = list(set(hid_fof_1+hid_fof_2 + both_hidden))

    try:
        hidden_friends.remove(user1_id)
    except:
        pass

    try:
        hidden_friends.remove(user2_id)
    except:
        pass

    edge_list = []
    for edge in G.edges():
        if (edge[0] in hid_1 or edge[1] in hid_1) and edge not in user2_G.edges(): 
            edge_list.append(edge)
        elif (edge[0] in hid_2 or edge[1] in hid_2) and edge not in user1_G.edges():
            edge_list.append(edge)
        elif edge[0] in hidden_friends or edge[1] in hidden_friends:
            edge_list.append(edge)
    remove_myselves = []
    for edge in G.edges():
        if edge[0] == user1_id or edge[1] == user2_id or edge[1] == user1_id or edge[0] == user2_id:
            remove_myselves.append(edge)
            G.remove_edge(edge[0], edge[1])
    for edge in remove_myselves:
        try:
            edge_list.remove(edge)
        except:
            continue
    G.remove_node(user1_id)
    G.remove_node(user2_id)
    return G, hidden_friends, edge_list


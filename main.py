import vk
import json
import networkx as nx
import matplotlib.pyplot as plt
import tqdm
import friends
import form_mutual_graph

with open('users.ids', 'r') as f:
    lines = f.readlines()
    user1_id = int(lines[0].strip())
    user2_id = int(lines[1].strip())

user1_G, hid_1 = friends.form_graph(user1_id, 1)
user2_G, hid_2 = friends.form_graph(user2_id, 2)
G = form_mutual_graph.merge_graphs(user1_G, user2_G) 
hidden_friends = list(set(hid_1+hid_2))
edge_list = []
d = dict(G.degree)
for edge in G.edges():
    if edge[0] in hidden_friends or edge[1] in hidden_friends:
        edge_list.append(edge)
pos1 = nx.kamada_kawai_layout(G)
spec_node_size = [d[user1_id] * 3, d[user2_id] * 3]
nx.draw_networkx_nodes(G, pos1, node_size=[v * 3 for v in d.values()], node_color="tab:blue")
nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="tab:red")
nx.draw_networkx_edges(G, pos1)
nx.draw_networkx_edges(G, pos1, edgelist=edge_list, edge_color='tab:red')
plt.show()
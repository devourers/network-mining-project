import vk
import networkx as nx
import matplotlib.pyplot as plt
import friends
import form_mutual_graph
import connection

#redo -- draw two same graphs for better view
plt.tight_layout()
with open('users.ids', 'r') as f:
    lines = f.readlines()
    user1_id = int(lines[0].strip())
    user2_id = int(lines[1].strip())

vk_api = connection.connect()


user1_G, hid_1 = friends.form_graph(user1_id, 1, vk_api)
user2_G, hid_2 = friends.form_graph(user2_id, 2, vk_api)

G = form_mutual_graph.merge_graphs(user1_G, user2_G)
G = form_mutual_graph.finish_graph(G, vk_api)

hidden_friends = list(set(hid_1+hid_2))

try:
    hidden_friends.remove(user1_id)
except:
    pass

try:
    hidden_friends.remove(user2_id)
except:
    pass

edge_list = []
d = dict(G.degree)
for edge in G.edges():
    if edge[0] in hidden_friends or edge[1] in hidden_friends:
        edge_list.append(edge)

pos1 = nx.kamada_kawai_layout(G)
other_edges = [edge for edge in G.edges() if edge not in edge_list]
other_nodes = [node for node in G.nodes() if node not in hidden_friends]
spec_node_size = [d[user1_id] * 3, d[user2_id] * 3]
hidden_node_sizes = [3*d[v] for v in hidden_friends]
normal_node_sizes = [3*d[v] for v in other_nodes]
nx.draw_networkx_nodes(G, pos1, nodelist=other_nodes, node_size=normal_node_sizes, node_color="tab:blue")
nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
nx.draw_networkx_edges(G, pos1, edgelist=other_edges)
plt.savefig("without_hidden.png", format = "PNG")
#second graph -- with hidden friends
nx.draw_networkx_nodes(G, pos1, nodelist=hidden_friends, node_size=hidden_node_sizes, node_color="yellow")
nx.draw_networkx_edges(G, pos1, edgelist=edge_list, edge_color='tab:red')
plt.savefig("with_hidden.png", format = "PNG")
plt.close()
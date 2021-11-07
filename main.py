import vk
import networkx as nx
import matplotlib.pyplot as plt
import friends
import form_mutual_graph

#redo -- draw two same graphs for better view
plt.tight_layout()
with open('users.ids', 'r') as f:
    lines = f.readlines()
    user1_id = int(lines[0].strip())
    user2_id = int(lines[1].strip())

user1_G, hid_1 = friends.form_graph(user1_id, 1)
user2_G, hid_2 = friends.form_graph(user2_id, 2)
G = form_mutual_graph.merge_graphs(user1_G, user2_G) 
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

spec_node_size = [d[user1_id] * 3, d[user2_id] * 3]

nx.draw_networkx_nodes(G, pos1, node_size=[v * 3 for v in d.values()], node_color="tab:blue")
nx.draw_networkx_nodes(G, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
nx.draw_networkx_edges(G, pos1)
nx.draw_networkx_edges(G, pos1, edgelist=edge_list, edge_color='tab:red')
plt.savefig("with_hidden.png", format = "PNG")
plt.close()
#second graph -- with hidden friends

G_hidden = nx.Graph()
for node in G.nodes():
    if node not in hidden_friends or (node in [user1_id, user2_id]):
        G_hidden.add_node(node)
for edge in G.edges():
    if edge[0] in G_hidden.nodes() and edge[1] in G_hidden.nodes():
        G_hidden.add_edge(edge[0], edge[1])



d = dict(G_hidden.degree)
pos1 = nx.kamada_kawai_layout(G_hidden)
spec_node_size = [d[user1_id] * 3, d[user2_id] * 3]
nx.draw_networkx_nodes(G_hidden, pos1, node_size=[v * 3 for v in d.values()], node_color="tab:blue")
nx.draw_networkx_nodes(G_hidden, pos1, nodelist=[user1_id, user2_id], node_size=spec_node_size,  node_color ="green")
nx.draw_networkx_edges(G_hidden, pos1)
plt.savefig("without_hidden.png", format = "PNG")
plt.close()
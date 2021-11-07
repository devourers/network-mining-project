import vk
import json
import networkx as nx
import matplotlib.pyplot as plt
import tqdm


import friends

user1_id = int(input("Input user1 id: "))
user2_id = int(input("Input user2 id: "))

user1_G = friends.form_graph(user1_id)
user2_G = friends.form_graph(user2_id)

pos1 = nx.kamada_kawai_layout(user1_G)
degree1 = nx.degree(user1_G)
nx.draw(user1_G, pos1)
plt.show()

pos2 = nx.kamada_kawai_layout(user2_G)
degree2 = nx.degree(user2_G)
nx.draw(user2_G, pos2)
plt.show()
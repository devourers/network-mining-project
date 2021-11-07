import vk
import json
import networkx as nx
import matplotlib.pyplot as plt
import tqdm

with open("access_token.auth", "r") as f:
    token = f.readline().strip()

version = "5.81"
vk_session = vk.Session(access_token=token)
vk_api = vk.API(vk_session)
print("Input user1 ID.")
user1_id = int(input())
G = nx.Graph()
friends_request = vk_api.friends.get(v=version, user_id=user1_id)
friends_1st_account = dict(friends_request)['items']
G.add_node(user1_id)
try:
    with open('user1.friends', 'r') as f:
        lines = f.readlines()
        for line in lines:
            friends_1st_account.append(int(line.strip()))
except:
    print("No file 'user1.friends' was found, assuming user1 has no hidden friends.")

for i in range(len(friends_1st_account)):
    G.add_node(friends_1st_account[i])
    G.add_edge(user1_id, friends_1st_account[i])

log = ""
for user in tqdm.tqdm(friends_1st_account):
    try:
        curr_friends = dict(vk_api.friends.get(v=version, user_id=user))['items']
        for friend in curr_friends:
            if friend not in G.nodes():
                G.add_node(friend)
            G.add_edge(user, friend)
    except:
        log += "Private data on user" + str(user) + "\n"

print("Finished generating friend graph. Across " + str(len(friends_1st_account)) +" accounts following were private")
print(log)

pos = nx.kamada_kawai_layout(G)
degree = nx.degree(G)
nx.draw(G, pos)
plt.show()
import vk
import networkx as nx
import matplotlib.pyplot as plt
import tqdm
import random

def form_sample(size, init_sample):
    res = []
    n = len(init_sample)
    if size > n:
        return init_sample
    else:
        for i in range(size):
            elem = random.choice(init_sample)
            if elem not in res:
                res.append(elem)
        return res


def form_graph(user1_id, friends_file, vk_api):
    fr_fl = 'user'
    fr_fl += str(friends_file)
    fr_fl += '.friends'
    hidden_friends = []
    version = "5.81"
    G = nx.Graph()
    friends_request = vk_api.friends.get(v=version, user_id=user1_id)
    friends_1st_account = dict(friends_request)['items']
    G.add_node(user1_id)
    try:
        with open(fr_fl, 'r') as f:
            lines = f.readlines()
            for line in lines:
                friends_1st_account.append(int(line.strip()))
                hidden_friends.append(int(line.strip()))
    except:
        print("No file" + fr_fl + "was found, assuming user has no hidden friends.")

    for i in range(len(friends_1st_account)):
        G.add_node(friends_1st_account[i])
        G.add_edge(user1_id, friends_1st_account[i])

    log = ""
    log_num = 0
    for user in tqdm.tqdm(friends_1st_account):
        try:
            curr_friends = form_sample(5, dict(vk_api.friends.get(v=version, user_id=user))['items'])
            for friend in curr_friends:
                if friend not in G.nodes():
                    G.add_node(friend)
                    if user in hidden_friends:
                        hidden_friends.append(friend)
                G.add_edge(user, friend)
        except:
            log += "Private data on user " + str(user) + "\n"
            log_num += 1
    labels = {}
    for node in G.nodes():
        if node in hidden_friends:
            labels.update({node : 1})
        else:
            labels.update({node : 0})
    nx.set_node_attributes(G, labels, "label")
    print("Finished generating friend graph. Across " + str(len(friends_1st_account)) +" accounts following " + str(log_num) +" were private")
    print(log)
    return G, hidden_friends
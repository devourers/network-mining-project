import friends
import connection
import visualistaion
import analyze
import form_mutual_graph
import tqdm
import networkx as nx
import matplotlib.pyplot as plt

scores = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

def construct_users_map(vk_api, user1_id, user2_id, friends_sample_size, FoF_sample_size, user1_friends, user2_friends):
    G1 = friends.form_graph_sample(user1_id, vk_api, friends_sample_size, FoF_sample_size, user1_friends)
    G2 = friends.form_graph_sample(user2_id, vk_api, friends_sample_size, FoF_sample_size, user2_friends)
    G = form_mutual_graph.merge_graphs(G1, G2, logging=False)
    #G = form_mutual_graph.finish_graph(G, vk_api, logging=False) #do i need it?
    return G

def find_closest_path(G, user1_id, user2_id):
    try:
        return nx.shortest_path_length(G, source=user1_id, target=user2_id)
    except:
        return -1


def count_netstalking_coef(vk_api, user1_id, user2_id, friends_sample_size, FoF_sample_size, repeat_counter, user1_friends, user2_friends):
    max_score = repeat_counter * scores[1]
    final_score = 0
    print("Counting... \n friends_sample_size=" + str(friends_sample_size) + " , FoF_sample_size=" + str(FoF_sample_size))
    for l in tqdm.tqdm(range(repeat_counter)):
        G = construct_users_map(vk_api, user1_id, user2_id, friends_sample_size, FoF_sample_size, user1_friends, user2_friends)
        curr_score = find_closest_path(G, user1_id, user2_id)
        '''
        Drawing of generated networks
        if (l == 0 or l == 3 ) and (friends_sample_size == 5 or friends_sample_size == 10 or friends_sample_size == 45) and curr_score != 0:
            plt.figure()
            plt.tight_layout()
            #ll = nx.kamada_kawai_layout(G)
            nx.draw(G)
            plt.savefig("netstalking_networks/" + str(l) + ".jpg")
            plt.close()
        '''
        try:
            final_score += scores[curr_score]
        except:
            final_score += 0

    return final_score/max_score

def get_netstalking_coef_plot(coefs, vk_api, user1_id, user2_id, repeat_counter, user1_friends, user2_friends):
    res = [[i/len(coefs), 0] for i in range(len(coefs))]
    i = 0
    for coef in coefs:
        curr_res = count_netstalking_coef(vk_api, user1_id, user2_id, coef[0], coef[1], repeat_counter, user1_friends, user2_friends)
        res[i][1] = curr_res
        i += 1
    return res
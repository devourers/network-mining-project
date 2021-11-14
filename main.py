import visualistaion
import analyze
import friends
import form_mutual_graph
import connection
import netstalking
import os
import numpy as np

version = "5.81"

def main(FoF_sample_size, graph_name):
    with open('users.ids', 'r') as f:
        lines = f.readlines()
        user1_id = int(lines[0].strip())
        user2_id = int(lines[1].strip())

    G, hidden_friends, edge_list = form_mutual_graph.construct_graph(user1_id, user2_id, FoF_sample_size)
    pos1 = visualistaion.form_kawada_kawai(G)
    try:
        os.mkdir(graph_name)
    except:
        pass
    visualistaion.draw_both_graphs(G, hidden_friends, edge_list, user1_id, user2_id, pos1, graph_name)
    with_hidden, without_hidden = analyze.construct_two_graphs(G, edge_list, hidden_friends)
    analyze.get_main_info(with_hidden, graph_name)
    analyze.get_main_info(without_hidden, graph_name, wo_hid=True)
    visualistaion.visualise_clustering(G, graph_name, with_hidden, pos1, user1_id, user2_id)
    visualistaion.visualise_clustering(G, graph_name, without_hidden, pos1, user1_id, user2_id, wo_hid=True)
    colors, widths = analyze.largest_cliques(G)
    size = np.unique(colors[0], axis=0, return_counts=True)[1][0]
    visualistaion.visualize_cliques(G, pos1, size, colors, widths, graph_name)

def netstalking_demo():
    vk_api = connection.connect()
    with open('user.ids', 'r') as f:
        lines = f.readlines()
        user1_id = int(lines[0].strip())
        user2_id = int(lines[1].strip())
    coefs = [[5, 5], [10, 5], [10, 10], [15, 10], [15, 15], [20, 15], [20,20], [25, 20], \
            [25, 25], [30, 25], [30, 30], [35, 35], [40, 40], [45, 45], [50, 50], \
            [60, 60], [70, 70], [80, 80], [90, 90], [100, 100], [100, 5]]
    repeat_counter = 1000
    user1_friends = vk_api.friends.get(v=version, user_id=user1_id)
    user2_friends = vk_api.friends.get(v=version, user_id=user2_id)
    res = netstalking.get_netstalking_coef_plot(coefs, vk_api, user1_id, user2_id, repeat_counter, user1_friends, user2_friends)
    visualistaion.visualise_netstalking_coeficients(res, coefs)
    

if __name__ == '__main__':
    print("Please input what method you would like to try: main or netstalking_demo.")
    method = str(input())
    if method == 'main':
        print("Chosen main. Please specify FoF (friends of friends) sample size:")
        FoF_sample_size = int(input())
        print("Please input your ego network name (it will be used as a name for the folder where everything will be saved.)")
        graph_name = str(input())
        main(FoF_sample_size, graph_name)
    elif method == 'netstalking_demo':
        print("Running netstalker demo...")
        netstalking_demo()

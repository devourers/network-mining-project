import visualistaion
import analyze
import friends
import form_mutual_graph
import connection
import os



def main():
    with open('users.ids', 'r') as f:
        lines = f.readlines()
        user1_id = int(lines[0].strip())
        user2_id = int(lines[1].strip())

    G, hidden_friends, edge_list = form_mutual_graph.construct_graph(user1_id, user2_id, 5)
    pos1 = visualistaion.form_kawada_kawai(G)
    graph_name = "mine_network"
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

if __name__ == '__main__':
    main()

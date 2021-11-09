import visualistaion
import analyze
import friends
import form_mutual_graph
import connection



def main():
    with open('users.ids', 'r') as f:
        lines = f.readlines()
        user1_id = int(lines[0].strip())
        user2_id = int(lines[1].strip())

    G, hidden_friends, edge_list = form_mutual_graph.construct_graph(user1_id, user2_id, 5)
    visualistaion.draw_both_graphs(G, hidden_friends, edge_list, user1_id, user2_id)
    analyze.get_main_info(G, "test")

if __name__ == '__main__':
    main()

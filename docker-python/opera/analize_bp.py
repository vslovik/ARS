import networkx as nx
import matplotlib.pyplot as plt


def draw(input_file, output_file, title, weighted=None):

    if weighted:
        graph1 = nx.Graph()
        graph2 = nx.Graph()
        graph3 = nx.Graph()
    else:
        graph1 = nx.MultiGraph()
        graph2 = nx.MultiGraph()
        graph3 = nx.MultiGraph()
    with open(input_file, 'r') as lines:
        for line in lines:
            print(line)
            arr = line.split(';')
            if len(arr) > 1:
                graph1.add_node(arr[0])
                graph2.add_node(arr[1])
                if weighted:
                    graph3.add_edge(arr[0],arr[1], weight=arr[2])
                else:
                    graph3.add_edge(arr[0],arr[1])

    try:
        pos = nx.nx_agraph.graphviz_layout(graph3)
    except:
        pos = nx.spring_layout(graph3, iterations=20)

    plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(20, 20))

    nx.draw_networkx_nodes(graph1, pos, node_color='b', alpha=0.5, node_size=20)
    nx.draw_networkx_nodes(graph2, pos, node_color='r', alpha=0.5, node_size=20)
    nx.draw_networkx_edges(graph3, pos, alpha=0.5, node_size=0, width=0.2, edge_color='k')

    plt.title(title, fontdict={'color': 'k', 'fontsize': 14})

    # font = {'color': 'k', 'fontsize': 12}
    # plt.text(0.5, 0.95, "edge width = # games played",
    #          horizontalalignment='center',
    #          transform=plt.gca().transAxes, fontdict=font)
    #
    # plt.text(0.5, 0.90, "node size = # games won",
    #          horizontalalignment='center',
    #          transform=plt.gca().transAxes, fontdict=font)

    plt.axis('off')
    plt.savefig(output_file, dpi=75)
    plt.show()


def info(graph):
    degree = sorted(nx.degree(graph).items(),
                    key=lambda x: x[1],
                    reverse=True)

    avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))

    (max_node, max_value) = degree[0]
    (min_node, min_value) = degree[len(degree) - 1]

    # h = nx.degree_histogram(graph)
    # print(h)
    # print(nx.info(graph))

    print('Number of nodes: {0}'.format(nx.number_of_nodes(graph)))
    print('Number of edges: {0}'.format(nx.number_of_edges(graph)))

    print('Degree:')
    print('Avg: {0}'.format(round(avg, 4)))
    print('Max: {1} ({0})'.format(max_node, max_value))
    print('Min: {1} ({0})'.format(min_node, min_value))

    print('Density: {}'.format(round(nx.density(graph), 4)))


def maximal_independent_set(graph):
    print(nx.maximal_independent_set(graph))


def distances(graph):
    print(nx.center(graph))
    print(nx.diameter(graph))
    print(nx.eccentricity(graph))
    print(nx.periphery(graph))
    print(nx.radius(graph))


def communities(graph):
    print(nx.core_number(graph))
    comm = nx.k_clique_communities(graph, 10)
    for c in comm:
        print("\n\n\n")
        print(c)


# Return single cast
def cliques(graph):
    cliques = nx.find_cliques(graph)
    for c in cliques:
        print("\n\n\n")
        for e in c:
            print(e)


def connectivity(graph):
    print(nx.is_connected(graph))
    print(nx.number_connected_components(graph))
    cc = list(nx.connected_component_subgraphs(graph))
    for c in cc:
        print("\n\n\n")
        for e in c:
            print(e)
        print('Center: {0}\n\n\n'.format(nx.center(c)))
        print('Diameter: {0}\n\n\n'.format(nx.diameter(c)))
        print('Eccentricity: {0}'.format(nx.eccentricity(c)))
        print('Periphery: {0}'.format(nx.periphery(c)))
        print('Radius: {0}'.format(nx.radius(c)))
        nx.draw_networkx(c,
                         font_size=8,
                         node_size=20,
                         with_labels=False,
                         node_color='b',
                         alpha=0.5)
        plt.show()
        break


def neighbor(graph):
    print(nx.average_neighbor_degree(graph))

#draw("/vagrant/data/singer_title.csv", "singer_title.png", "Opera singers vs opera graph: 2008 - 2016")
#draw("/vagrant/data/singer_title_weighted.csv", "singer_title_weighted.png", "Opera singers vs opera weighted graph: 2008 - 2016",True)
draw("/vagrant/data/singer_role.csv", "singer_role.png", "Opera singers vs roles graph: 2008 - 2016")
#draw("/vagrant/data/singer_role_weighted.csv", "singer_role_weighted.png", "Opera singers vs roles weighted graph: 2008 - 2016",True)





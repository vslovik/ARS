import networkx as nx
import matplotlib.pyplot as plt


def draw(input, output, title):
    graph = nx.read_edgelist(input, delimiter=";", nodetype=str)
    try:
        pos = nx.nx_agraph.graphviz_layout(graph)
    except:
        pos = nx.spring_layout(graph, iterations=20)

    plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(10, 10))

    nx.draw_networkx_nodes(graph, pos, node_color='b', alpha=0.5, node_size=20)
    nx.draw_networkx_edges(graph, pos, alpha=0.5, node_size=0, width=0.1, edge_color='k')
    # nx.draw_networkx_labels(graph,pos,fontsize=8)

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
    plt.savefig(output, dpi=75)
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



#draw("/vagrant/data/singer_singer.csv", "singer_singer.png", "Opera singers connection graph: 2008 - 2016")
#draw("/vagrant/data/singer_title.csv", "singer_title.png", "Opera singers vs opera graph: 2008 - 2016")
#draw("/vagrant/data/singer_role.csv", "singer_role.png", "Opera singers vs roles graph: 2008 - 2016")
draw("/vagrant/data/singer_event.csv", "singer_event.png", "Opera singers vs performance graph: 2008 - 2016")
#OperaGraph.info(OperaGraph())
#OperaGraph.maximal_independent_set(OperaGraph())
#OperaGraph.distances(OperaGraph())
#OperaGraph.communities(OperaGraph())
#OperaGraph.cliques(OperaGraph())
#OperaGraph.connectivity(OperaGraph())
#OperaGraph.neighbor(OperaGraph())




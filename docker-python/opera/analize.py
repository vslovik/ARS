import networkx as nx
import matplotlib.pyplot as plt


def draw(input_file, output_file, title, weighted=None):
    if weighted:
        graph = nx.read_weighted_edgelist(input_file, delimiter=";", nodetype=str, encoding='utf-8')
    else:
        graph = nx.read_edgelist(input_file, delimiter=";", nodetype=str, create_using=nx.MultiGraph())

    try:
        pos = nx.nx_agraph.graphviz_layout(graph)
    except:
        pos = nx.spring_layout(graph, iterations=20)

    plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(20, 20))

    nx.draw_networkx_nodes(graph, pos, node_color='b', alpha=0.5, node_size=20)
    nx.draw_networkx_edges(graph, pos, alpha=0.5, node_size=0, width=0.1, edge_color='k')

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
    degree = sorted(nx.degree(graph).items(), key=lambda x: x[1], reverse=True)
    avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))

    (max_node, max_value) = degree[0]
    (min_node, min_value) = degree[len(degree) - 1]

    # h = nx.degree_histogram(graph) # print(h)
    
    inf = list()
    inf.append('Number of nodes: {0}'.format(nx.number_of_nodes(graph)))
    inf.append('Number of edges: {0}'.format(nx.number_of_edges(graph)))
    inf.append('Degree:')
    inf.append('Avg: {0}'.format(round(avg, 4)))
    inf.append('Max: {1} ({0})'.format(max_node, max_value))
    inf.append('Min: {1} ({0})'.format(min_node, min_value))
    inf.append('Density: {}'.format(round(nx.density(graph), 4)))
    
    return inf


def distances(graph):
    inf = list()
    inf.append('infances:')
    inf.append('Center: {}'.format(nx.center(graph)))
    inf.append('Diameter: {}'.format(nx.diameter(graph)))
    inf.append('Eccentricity: {}'.format(nx.eccentricity(graph)))
    inf.append('Periphery: {}'.format(nx.periphery(graph)))
    inf.append('Radius: {}'.format(nx.radius(graph)))
    
    return inf


def neighbor(graph):
    inf = list()
    inf.append('Average neighbor degree: {}'.format(nx.average_neighbor_degree(graph)))
    return info


def maximal_independent_set(graph):
    print(nx.maximal_independent_set(graph))
    
    
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


def connectivity(graph, output_file):
    inf = list()
    inf.append('Connectivity:')
    inf.append('Connected: {0}'.format(nx.is_connected(graph)))
    inf.append('Number of connected components: {0}'.format(nx.number_connected_components(graph)))
    connected_components = list(nx.connected_component_subgraphs(graph))
    i = 0
    for c in connected_components:
        inf.append('Connected component {0}'.format(i))
        # for e in c:
        #     print(e)
        inf.append('Center: {0}\n\n\n'.format(nx.center(c)))
        inf.append('Diameter: {0}\n\n\n'.format(nx.diameter(c)))
        inf.append('Eccentricity: {0}'.format(nx.eccentricity(c)))
        inf.append('Periphery: {0}'.format(nx.periphery(c)))
        inf.append('Radius: {0}'.format(nx.radius(c)))
        nx.draw_networkx(c,
                         font_size=8,
                         node_size=20,
                         with_labels=False,
                         node_color='b',
                         alpha=0.5)
        plt.axis('off')
        plt.savefig(output_file, dpi=75)
        plt.show()
        i += 1



#draw("/vagrant/data/singer_singer.csv", "singer_singer.png", "Opera singers vs roles graph: 2008 - 2016")
draw("/vagrant/data/singer_singer_weighted.csv", "singer_singer_weighted.png", "Opera singers vs roles weighted graph: 2008 - 2016",True)





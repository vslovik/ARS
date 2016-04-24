import networkx as nx
import matplotlib.pyplot as plt


class OperaGraph:
    def __init__(self):
        self.G = nx.read_edgelist("/vagrant/data/r.csv",
                                  delimiter=",",
                                  nodetype=str)

    def draw(self):

        try:
            pos=nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos=nx.spring_layout(self.G,iterations=20)

        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(10,10))

        # nx.draw_networkx(self.G,
        #                  font_size=8,
        #                  node_size=20,
        #                  with_labels=False,
        #                  node_color='b',
        #                  alpha=0.5)

        nx.draw_networkx_nodes(self.G,pos,node_color='b',alpha=0.5, node_size=20)
        nx.draw_networkx_edges(self.G,pos,alpha=0.5,node_size=0,width=0.1,edge_color='k')
        #nx.draw_networkx_labels(self.G,pos,fontsize=8)


        font = {'color':'k','fontsize':14}
        plt.title("Opera singers graph: 2008 - 2016", fontdict=font)

        font = {'color':'k','fontsize':12}
        plt.text(0.5, 0.95, "edge width = # games played",
        horizontalalignment='center',
        transform=plt.gca().transAxes, fontdict=font)

        plt.text(0.5, 0.90,  "node size = # games won",
        horizontalalignment='center',

        transform=plt.gca().transAxes, fontdict=font)

        plt.axis('off')
        plt.savefig("singers.png",dpi=75)
        plt.show()

    def info(self):
        degree = sorted(nx.degree(self.G).items(),
                        key=lambda x: x[1],
                        reverse=True)

        avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))

        (max_node, max_value) = degree[0]
        (min_node, min_value) = degree[len(degree) - 1]

        #h = nx.degree_histogram(self.G)
        #print(h)
        #print(nx.info(self.G))

        print('Number of nodes: {0}'.format(nx.number_of_nodes(self.G)))
        print('Number of edges: {0}'.format(nx.number_of_edges(self.G)))

        print('Degree:')
        print('Avg: {0}'.format(round(avg, 4)))
        print('Max: {1} ({0})'.format(max_node, max_value))
        print('Min: {1} ({0})'.format(min_node, min_value))

        print('Density: {}'.format(round(nx.density(self.G),4)))

    def maximal_independent_set(self):
        print(nx.maximal_independent_set(self.G))

    def distances(self):
        print(nx.center(self.G))
        print(nx.diameter(self.G))
        print(nx.eccentricity(self.G))
        print(nx.periphery(self.G))
        print(nx.radius(self.G))

    def communities(self):
        print(nx.core_number(self.G))
        comm = nx.k_clique_communities(self.G, 10)
        for c in comm:
            print("\n\n\n")
            print(c)

    # Return single cast
    def cliques(self):
        cliques = nx.find_cliques(self.G)
        for c in cliques:
            print("\n\n\n")
            for e in c:
                print(e)

    def connectivity(self):
        print(nx.is_connected(self.G))
        print(nx.number_connected_components(self.G))
        cc = list(nx.connected_component_subgraphs(self.G))
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

    def neighbor(self):
        print(nx.average_neighbor_degree(self.G))


OperaGraph.draw(OperaGraph())
#OperaGraph.info(OperaGraph())
#OperaGraph.maximal_independent_set(OperaGraph())
#OperaGraph.distances(OperaGraph())
#OperaGraph.communities(OperaGraph())
#OperaGraph.cliques(OperaGraph())
#OperaGraph.connectivity(OperaGraph())
#OperaGraph.neighbor(OperaGraph())




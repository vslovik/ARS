import networkx as nx
import matplotlib.pyplot as plt
import os

"""www.gbopera.it graph analyse"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "analyzer"


class Analyzer(object):

    SINGER_GRAPH_FILE = '/data/singer_singer/weighted/SINGER_SINGER.csv'
    SINGER_DICT = '/data/singer_singer/weighted/SINGER_DICT.csv'

    def __init__(self):
        self.G = nx.read_weighted_edgelist(
            Analyzer.get_data_dir() + Analyzer.SINGER_GRAPH_FILE,
            delimiter=';',
            encoding='utf-8'
        )
        self.G.remove_edges_from(self.G.selfloop_edges())
        self.singer_dict = Analyzer.read_dict(Analyzer.get_data_dir() + Analyzer.SINGER_DICT)

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/../..'

    @staticmethod
    def read_dict(dictionary_file):
        d = dict()
        fh = open(dictionary_file)
        for line in fh:
            items = line.split('|')
            d[int(items[0])] = '|'.join(items[1:])
        return d

    def get_graph(self):
        return self.G

    def inform(self):
        self.plot_degree_histogram(self.G)

        inf = self.info(self.G)
        print(inf)
        # if nx.is_connected(self.G):
        #     inf += self.distances(self.G)
        # inf += self.connectivity()

    def inform_sub_graph(self, graph):
        self.plot_degree_histogram(graph)

        inf = self.info(graph)
        n = graph.number_of_nodes()
        er = nx.erdos_renyi_graph(n, 0.05)
        inf += self.info(er, 'ER')
        ba = nx.barabasi_albert_graph(n, 5)
        inf += self.info(ba, 'BA')

        inf += self.distances(graph, er, ba)

    @staticmethod
    def info(graph, title=None):
        degree = sorted(nx.degree(graph).items(), key=lambda x: x[1], reverse=True)
        avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))
        (max_node, max_value) = degree[0]
        (min_node, min_value) = degree[len(degree) - 1]
        inf = list()
        if not title:
            inf.append('Number of nodes: {0}'.format(nx.number_of_nodes(graph)))
            inf.append('Number of edges: {0}'.format(nx.number_of_edges(graph)))
            inf.append('Is connected: {0}'.format(nx.is_connected(graph)))
        if title:
            inf.append(title)
        inf.append('Degree:')
        inf.append('Avg: {0}'.format(round(avg, 4)))
        inf.append('Max: {1} ({0})'.format(max_node, max_value))
        inf.append('Min: {1} ({0})'.format(min_node, min_value))
        inf.append('Density: {}'.format(round(nx.density(graph), 4)))
        return inf

    @staticmethod
    def plot_degree_histogram(graph):
        plt.rcParams['text.usetex'] = False
        plt.loglog(nx.degree_histogram(graph),'b-', marker='o')

        n = graph.number_of_nodes()
        er = nx.erdos_renyi_graph(n, 0.05)
        ba = nx.barabasi_albert_graph(n, 5)

        plt.loglog(nx.degree_histogram(er), 'r-', marker='o')
        plt.loglog(nx.degree_histogram(ba), 'k-', marker='o')

        plt.xlabel("degree")
        plt.ylabel("rank")
        plt.savefig('degree_histogram.png', dpi=75, transparent=False)

    @staticmethod
    def distances(graph, er=None, ba=None):
        inf = list()
        inf.append('Center: \n')
        names = nx.center(graph)
        names.sort()
        for name in names:
            inf.append('{0}'.format(name.rstrip()))
        if er and ba:
            inf.append('Diameter: {0} (ER: {1}, BA: {2})\n'.format(nx.diameter(graph), nx.diameter(er), nx.diameter(ba)))
        else:
            inf.append('Diameter: {0}\n'.format(nx.diameter(graph)))
        inf.append('Periphery: \n')
        names = nx.periphery(graph)
        names.sort()
        for name in nx.periphery(graph):
            inf.append('{0}'.format(name.rstrip()))
        if er and ba:
            inf.append('Radius: {0} (ER: {1}, BA: {2})\n'.format(nx.radius(graph), nx.radius(er), nx.radius(ba)))
            inf.append('Average shortest path length: {0} (ER: {1}, BA: {2})\n'.format(
                nx.average_shortest_path_length(graph),
                nx.average_shortest_path_length(er),
                nx.average_shortest_path_length(ba)
            ))
        else:
            inf.append('Radius: {0}\n'.format(nx.radius(graph)))
            inf.append('Radius: {0}\n'.format(nx.average_shortest_path_length(graph)))
        return inf

    def connectivity(self):
        inf = list()
        inf.append('Connectivity:')
        inf.append('Connected: {0}'.format(nx.is_connected(self.G)))
        inf.append('Number of connected components: {0}'.format(nx.number_connected_components(self.G)))
        connected_components = list(nx.connected_component_subgraphs(self.G))
        i = 0
        for component in connected_components:
            inf.append('Connected component {0}'.format(i))
            Analyzer.distances(component)
            self.inform_sub_graph(component)
            inf.append('Average clustering: {0}'.format(nx.average_clustering(component)))
            i += 1
            break # only first component is interesting
        return inf

Analyzer().inform()
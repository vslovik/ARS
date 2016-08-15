import networkx as nx
import matplotlib.pyplot as plt
import os

"""www.gbopera.it graph analyser"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"


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
        return os.getcwd()

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
        return self.get_graph_info(self.G)

    def get_graph_info(self, graph):
        self.plot_degree_histogram(graph)

        inf = self.info(graph)
        n = graph.number_of_nodes()
        er = nx.erdos_renyi_graph(n, 0.005)
        inf += self.info(er, 'ER')
        ba = nx.barabasi_albert_graph(n, 10)
        inf += self.info(ba, 'BA')

        return inf

    def info(self, graph, title=None):
        degree = sorted(nx.degree(graph).items(), key=lambda x: x[1], reverse=True)
        print('Highest degree nodes: ')
        if not title:
            for (node, value) in degree:
                print('{}:{}'.format(self.singer_dict[int(node)].split('|')[0], str(value)))
                if value < 90:
                    break

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

    def connectivity(self):
        components = list(nx.connected_component_subgraphs(self.G))
        print('Connected components number: ')
        print(len(components))
        giant = components.pop(0)
        print('Giant component radius: ')
        print(nx.radius(giant))
        print('Giant component diameter: ')
        print(nx.diameter(giant))
        center = nx.center(giant)
        print('Giant component center: ')
        for i in xrange(len(center)):
            print(self.singer_dict[int(center[i])].split('|')[0])
        inf = self.get_graph_info(giant)
        for i in xrange(len(inf)):
            print(inf[i])

Analyzer().inform()
#Analyzer().connectivity()
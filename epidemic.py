import networkx as nx
import matplotlib.pyplot as plt
import os
from Queue import PriorityQueue
import time
import random

"""www.gbopera.it graph cliques & egos spy"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"


def timeit(method):

    def timed(*argst, **kwt):
        ts = time.time()
        result = method(*argst, **kwt)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, argst, kwt, te-ts)
        return result

    return timed


class OperaEpidemics(object):

    @staticmethod
    def get_data_dir():
        return os.getcwd()

    @staticmethod
    def get_hubs(graph, seed_size):
        degree = sorted(nx.degree(graph).items(), key=lambda x: x[1], reverse=True)
        nodes = []
        for (node, degree) in degree[0:seed_size]:
            nodes.append(node)
        return nodes

    @staticmethod
    def get_center_ego(graph):
        bt = nx.betweenness_centrality(graph)
        print(bt)
        for (node, betweenness) in sorted(bt.items(), key=lambda x: x[1], reverse=True):
            nodes = nx.ego_graph(graph, node).nodes()
            print(nodes)
            return nodes

    @staticmethod
    def get_centers(graph):
        bt = nx.betweenness_centrality(graph)
        centers = []
        i = 0
        for (node, betweenness) in sorted(bt.items(), key=lambda x: x[1], reverse=True):
            centers.append(node)
            i += 1
            if i > 100:
                return centers
        return centers

    @staticmethod
    def get_random_seed(graph, seed_size):
        n = graph.number_of_nodes()
        if seed_size > n:
            raise Exception('Invalid seed size')
        seed = set()
        while len(seed) < seed_size:
            index = random.randint(0, n - 1)
            seed.add(graph.nodes()[index])
        return list(seed)

    @staticmethod
    def get_opera_graph():
        graph = nx.read_weighted_edgelist(
            os.getcwd() + '/data/singer_singer/weighted/SINGER_SINGER.csv',
            delimiter=';',
            nodetype=int
        )
        graph.remove_edges_from(graph.selfloop_edges())
        components = list(nx.connected_component_subgraphs(graph, True))
        giant = components.pop(0)
        degree = sorted(nx.degree(giant).items(), key=lambda x: x[1], reverse=True)
        avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))
        print(avg) # 20.9834926151
        return giant

    @staticmethod
    def plot_spread_size_distribution(thresholds, distributions, colors, filename, xaxis_name='threshold'):
        for i in xrange(len(distributions)):
            plt.plot(thresholds, distributions[i], linestyle="solid", color=colors[i])
        plt.rcParams['text.usetex'] = False
        plt.xlabel(xaxis_name)
        plt.ylabel('spread size, nodes')
        plt.savefig(filename, dpi=75, transparent=False)
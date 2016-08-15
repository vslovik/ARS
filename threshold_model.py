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


class ThresholdModel(object):

    RESULT_DIR = '/data/threshold_model/'

    def __init__(self, graph, threshold=0.5, seed_size=100):
        if not graph.size():
            raise Exception('Invalid graph')
        if threshold >= 1:
            raise Exception('Invalid threshold')
        if seed_size >= graph.size():
            raise Exception('Invalid seed size')

        self.G = graph
        self.threshold = threshold
        self.seed_size = seed_size
        self.seed = []
        self.marked = dict()
        self.pq = PriorityQueue()

    @staticmethod
    def get_data_dir():
        return os.getcwd()

    def get_center(self):
        components = list(nx.connected_component_subgraphs(self.G))
        giant = components.pop(0)
        return nx.center(giant)

    def get_hubs(self):
        degree = sorted(nx.degree(self.G).items(), key=lambda x: x[1], reverse=True)
        nodes = []
        for (node, degree) in degree[0:self.seed_size]:
            nodes.append(node)
        return nodes

    @timeit
    def set_seed(self):
        seed = set()
        while len(seed) < self.seed_size:
            index = random.randint(1, self.G.number_of_nodes())
            seed.add(graph.nodes()[index])
        self.seed = list(seed)
        print('Seed: ')
        print(self.seed)
        for i in xrange(len(self.seed)):
            self.marked[self.seed[i]] = 1
        for i in xrange(len(self.seed)):
            self.enqueue_neighbors(self.seed[i])

    @timeit
    def enqueue_neighbors(self, node):
        print(node)
        neighbors = self.G.neighbors(node)
        for j in xrange(len(neighbors)):
            if neighbors[j] not in self.marked:
                self.pq.put(neighbors[j])

    @timeit
    def spread(self):
        self.set_seed()
        while not self.pq.empty():
            node = self.pq.get()
            if node not in self.marked:
                vote = self.vote(node)
                if vote:
                    self.marked[node] = 1
                    self.enqueue_neighbors(node)

    @timeit
    def vote(self, node):
        print(node)
        neighbors = self.G.neighbors(node)
        return float(len(set(neighbors).intersection(self.marked.keys()))) > self.threshold * float(len(neighbors))

    @timeit
    def draw(self, filename):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        print(self.marked.keys())
        not_seed = set(self.marked.keys()) - set(self.seed)
        not_marked = set(self.G.nodes()) - set(self.marked.keys()) - set(self.seed)

        nx.draw_networkx_nodes(self.G, pos, list(not_marked), alpha=0.2, node_size=20, node_color='grey')
        nx.draw_networkx_nodes(self.G, pos, list(not_seed), alpha=0.5, node_size=20, node_color='red', linewidths=0.)
        nx.draw_networkx_nodes(self.G, pos, self.seed, alpha=0.5, node_size=20, node_color='orange', linewidths=0.)
        nx.draw_networkx_edges(self.G, pos, alpha=0.2, node_size=0, width=0.1, edge_color='grey')

        plt.savefig(self.get_data_dir() + ThresholdModel.RESULT_DIR +
                    '_'.join([filename, str(self.threshold).replace('.',''), str(self.seed_size)]) , dpi=75, transparent=False)
        plt.close()


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

graph = get_opera_graph()

tm = ThresholdModel(get_opera_graph(), 0.2, 500)
tm.spread()
tm.draw('opera')

# n = graph.number_of_nodes()
# m = graph.number_of_edges()
#
# tm = ThresholdModel(nx.barabasi_albert_graph(n, 21), 0.1)
# tm.spread()
# tm.draw('ba')

# tm = ThresholdModel(nx.erdos_renyi_graph(n, m), 0.1)
# tm.spread()
# tm.draw('er')
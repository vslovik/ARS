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

    def __init__(self, graph, threshold=0.5, seed_size=200, seed_nodes=None):
        if not graph.size():
            raise Exception('Invalid graph')
        if threshold > 1:
            raise Exception('Invalid threshold')
        if seed_size >= graph.size():
            raise Exception('Invalid seed size')

        self.G = graph
        self.threshold = threshold
        self.seed_size = seed_size
        if seed_nodes:
            self.seed = seed_nodes
        else:
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

    def get_random_seed(self):
        seed = set()
        while len(seed) < self.seed_size:
            index = random.randint(0, self.G.number_of_nodes() - 1)
            seed.add(self.G.nodes()[index])
        return seed

    def set_seed(self):
        if not len(self.seed):
            seed = self.get_random_seed()
            self.seed = list(seed)
        for i in xrange(len(self.seed)):
            self.marked[self.seed[i]] = 1
        for i in xrange(len(self.seed)):
            self.enqueue_neighbors(self.seed[i])

    def enqueue_neighbors(self, node):
        neighbors = self.G.neighbors(node)
        for j in xrange(len(neighbors)):
            if neighbors[j] not in self.marked:
                self.pq.put(neighbors[j])

    def spread(self):
        self.set_seed()
        while not self.pq.empty():
            node = self.pq.get()
            if node not in self.marked:
                vote = self.vote(node)
                if vote:
                    self.marked[node] = 1
                    self.enqueue_neighbors(node)
        return len(self.marked)

    def vote(self, node):
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
        nx.draw_networkx_nodes(self.G, pos, self.seed, alpha=0.5, node_size=20, node_color='blue', linewidths=0.)
        nx.draw_networkx_edges(self.G, pos, alpha=0.2, node_size=0, width=0.1, edge_color='grey')

        plt.savefig(ThresholdModel.get_data_dir() + ThresholdModel.RESULT_DIR +
                    '_'.join([filename, str(self.threshold).replace('.',''), str(self.seed_size)]) , dpi=75, transparent=False)
        plt.close()

    @staticmethod
    def plot_spread_size_distribution(thresholds, o_sizes, ba_sizes=None, er_sizes=None):

        plt.plot(thresholds, o_sizes, linestyle="solid", color="blue")
        if ba_sizes:
            plt.plot(thresholds, ba_sizes, linestyle="solid", color="black")
        if er_sizes:
            plt.plot(thresholds, er_sizes, linestyle="solid", color="red")

        plt.rcParams['text.usetex'] = False
        plt.xlabel("threshold")
        plt.ylabel("spread size, nodes")
        plt.savefig(ThresholdModel.get_data_dir() + ThresholdModel.RESULT_DIR
                    + 'spread_size_distribution.png', dpi=75, transparent=False)


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


thresholds = [float(i)/100. for i in range(100)]

graph = get_opera_graph()
seed = ThresholdModel.get_hubs(graph, 500)
o_sizes = []
for i in xrange(len(thresholds)):
    o_sizes.append(ThresholdModel(graph, thresholds[i], 500, seed).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 10)
seed = ThresholdModel.get_center_ego(graph)
ba_sizes = []
for i in xrange(len(thresholds)):
    ba_sizes.append(ThresholdModel(graph, thresholds[i], 200, ThresholdModel.get_center_ego(graph)).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = ThresholdModel.get_center_ego(graph)
er_sizes = []
for i in xrange(len(thresholds)):
    er_sizes.append(ThresholdModel(graph, thresholds[i], 200, ThresholdModel.get_center_ego(graph)).spread())
print(er_sizes)

ThresholdModel.plot_spread_size_distribution(thresholds, o_sizes)
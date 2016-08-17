import networkx as nx
import matplotlib.pyplot as plt
from Queue import PriorityQueue
import time
import seed

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


class ThresholdModel(seed.OperaEpidemics):

    RESULT_DIR = '/data/threshold_model/'

    @timeit
    def __init__(self, graph, seed_nodes, threshold=0.5):
        if not graph.size():
            raise Exception('Invalid graph')
        if not len(seed_nodes):
            raise Exception('Invalid seed')
        if threshold > 1:
            raise Exception('Invalid threshold')

        self.G = graph
        self.threshold = threshold

        self.marked = dict()
        self.pq = PriorityQueue()

        for m in xrange(len(seed_nodes)):
            self.marked[seed_nodes[m]] = True
        for i in xrange(len(seed_nodes)):
            self.enqueue_neighbors(seed_nodes[i])

    def enqueue_neighbors(self, node):
        neighbors = self.G.neighbors(node)
        for j in xrange(len(neighbors)):
            if neighbors[j] not in self.marked:
                self.pq.put(neighbors[j])

    def spread(self):
        while not self.pq.empty():
            node = self.pq.get()
            if node not in self.marked:
                vote = self.vote(node)
                if vote:
                    self.marked[node] = True
                    self.enqueue_neighbors(node)
        return len(self.marked)

    def vote(self, node):
        neighbors = self.G.neighbors(node)
        return float(len(set(neighbors).intersection(self.marked.keys()))) > self.threshold * float(len(neighbors))

    @timeit
    def draw(self, filename, seed=None):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        if not seed:
            seed = []
        print(self.marked.keys())
        not_seed = set(self.marked.keys()) - set(seed)
        not_marked = set(self.G.nodes()) - set(self.marked.keys()) - set(seed)

        nx.draw_networkx_nodes(self.G, pos, list(not_marked), alpha=0.2, node_size=20, node_color='grey')
        nx.draw_networkx_nodes(self.G, pos, list(not_seed), alpha=0.5, node_size=20, node_color='red', linewidths=0.)
        nx.draw_networkx_nodes(self.G, pos, seed, alpha=0.5, node_size=20, node_color='blue', linewidths=0.)
        nx.draw_networkx_edges(self.G, pos, alpha=0.2, node_size=0, width=0.1, edge_color='grey')

        plt.savefig(ThresholdModel.get_data_dir() + ThresholdModel.RESULT_DIR +
                    '_'.join([filename, str(self.threshold).replace('.',''), str(len(seed))]), dpi=75, transparent=False)
        plt.close()


thresholds = [float(i)/100. for i in range(100)]

graph = ThresholdModel.get_opera_graph()
seed = ThresholdModel.get_hubs(graph, 500)
o_sizes = []
for i in xrange(len(thresholds)):
    o_sizes.append(ThresholdModel(graph, seed, thresholds[i]).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 10)
seed = ThresholdModel.get_center_ego(graph)
ba_sizes = []
for i in xrange(len(thresholds)):
    ba_sizes.append(ThresholdModel(graph, seed, thresholds[i]).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = ThresholdModel.get_center_ego(graph)
er_sizes = []
for i in xrange(len(thresholds)):
    er_sizes.append(ThresholdModel(graph, seed, thresholds[i]).spread())
print(er_sizes)

ThresholdModel.plot_spread_size_distribution(thresholds, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
                                             ThresholdModel.get_data_dir() + ThresholdModel.RESULT_DIR + 'spread_size_distribution.png')
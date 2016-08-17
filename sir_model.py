import networkx as nx
import matplotlib.pyplot as plt
import os
from Queue import PriorityQueue
import time
import random
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


class SIRModel(seed.OperaEpidemics):

    RESULT_DIR = '/data/sir_model/'
    REMOVED = False
    INFECTED = True

    def __init__(self, graph, seed_nodes, p=0.5, t=1):
        if not graph.size():
            raise Exception('Invalid graph')
        if not len(seed_nodes):
            raise Exception('Invalid seed')
        if p > 1 or p < 0:
            raise Exception('Invalid infection probability')

        self.G = graph
        self.p = p
        self.t = t

        self.touched = dict()
        self.pq = PriorityQueue()

        for i in xrange(len(seed_nodes)):
            self.touched[seed_nodes[i]] = SIRModel.INFECTED
        for i in xrange(len(seed_nodes)):
            self.pq.put((seed_nodes[i], 1))

    @timeit
    def spread(self):
        while not self.pq.empty():
            (node, t) = self.pq.get()

            neighbors = list(set(self.G.neighbors(node)))

            for i in xrange(len(neighbors)):
                s = neighbors[i]
                if s in self.touched:
                    continue
                if self.infect():
                    self.touched[s] = SIRModel.INFECTED
                    self.pq.put((s, 1))

            if t >= self.t + 1:
                print('OK')
                self.pq.put((node, t - 1))
            else:
                self.touched[node] = SIRModel.REMOVED

        #return len([x for x in self.touched.keys() if x == SIRModel.INFECTED])
        return len(self.touched.keys())

    def infect(self):
        r = random.uniform(0, 1)
        if r < self.p:
            return True
        return False

    @timeit
    def draw(self, filename, seed=None):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        print(self.touched.keys())

        if not seed:
            seed = []
        nx.draw_networkx_nodes(self.G, pos, list(set(self.G.nodes()) - set(self.touched.keys()) - set(seed)), alpha=0.2, node_size=20, node_color='grey')
        nx.draw_networkx_nodes(self.G, pos, list(set(self.touched.keys()) - set(seed)), alpha=0.5, node_size=20, node_color='red', linewidths=0.)
        nx.draw_networkx_nodes(self.G, pos, seed, alpha=0.5, node_size=20, node_color='blue', linewidths=0.)

        nx.draw_networkx_nodes(self.G, pos, [x for x in self.touched.keys() if x == SIRModel.REMOVED], alpha=0.5, node_size=20, node_color='black', linewidths=0.)

        nx.draw_networkx_edges(self.G, pos, alpha=0.2, node_size=0, width=0.1, edge_color='grey')

        plt.savefig(SIRModel.get_data_dir() + SIRModel.RESULT_DIR +
                    '_'.join([filename, str(self.p).replace('.',''), str(len(seed))]) , dpi=75, transparent=False)
        plt.close()


probabilities = [float(i)/100. for i in range(100)]
t = 1

graph = SIRModel.get_opera_graph()
seed = SIRModel.get_hubs(graph, 50)
o_sizes = []
for i in xrange(len(probabilities)):
    o_sizes.append(SIRModel(graph, seed, probabilities[i], t).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 1)
seed = SIRModel.get_hubs(graph, 50)
ba_sizes = []
for i in xrange(len(probabilities)):
    ba_sizes.append(SIRModel(graph, seed, probabilities[i], t).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = SIRModel.get_hubs(graph, 50)
er_sizes = []
for i in xrange(len(probabilities)):
    er_sizes.append(SIRModel(graph, seed, probabilities[i], t).spread())
print(er_sizes)

SIRModel.plot_spread_size_distribution(probabilities, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
                                       SIRModel.get_data_dir() + SIRModel.RESULT_DIR + 'spread_size_distribution.png')
import networkx as nx
import matplotlib.pyplot as plt
import os
from Queue import PriorityQueue
import time
import random
import seed

"""SIR model"""

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

        self.infected = dict()
        for i in xrange(len(seed_nodes)):
            self.infected[seed_nodes[i]] = self.t

        self.step = 1

    def get_infected(self):
        return [node for node in self.infected if self.infected[node]]

    @timeit
    def spread(self):
        while len(self.get_infected()):
            current_step = self.get_infected()
            while len(current_step):
                node = current_step.pop()
                neighbors = list(set(self.G.neighbors(node)))
                for i in xrange(len(neighbors)):
                    s = neighbors[i]
                    if s in self.infected:
                        continue
                    if self.infect():
                        self.infected[s] = self.t
                if self.infected[node] > 0:
                    self.infected[node] -= 1
            self.step += 1
            print(len(self.infected))

        return len(self.infected)

    def infect(self):
        r = random.uniform(0, 1)
        return r <= self.p

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
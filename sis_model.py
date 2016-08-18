import networkx as nx
import matplotlib.pyplot as plt
import os
from Queue import PriorityQueue
import time
import random
import seed

"""SIS model"""

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


class SISModel(seed.OperaEpidemics):

    RESULT_DIR = '/data/sis_model/'

    def __init__(self, graph, seed_nodes, p=0.5, t=1):
        if not graph.size():
            raise Exception('Invalid graph')
        if not len(seed_nodes):
            raise Exception('Invalid seed size')
        if p > 1:
            raise Exception('Invalid infection probability')

        self.G = graph
        self.p = p
        self.t = t

        self.infected = dict()
        self.pq = PriorityQueue()

        for i in xrange(len(seed_nodes)):
            self.infected[seed_nodes[i]] = True
        for i in xrange(len(seed_nodes)):
            self.pq.put((seed_nodes[i], 1))

    def get_infected(self):
        return self.infected

    @timeit
    def spread(self):
        count = 0

        while not self.pq.empty():
            infected_num = len(self.infected.keys())
            (node, t) = self.pq.get()
            neighbors = list(set(self.G.neighbors(node)))
            #print('{}:{}'.format(count, len(self.infected)))
            for i in xrange(len(neighbors)):
                s = neighbors[i]
                if s in self.infected:
                    continue
                if self.infect():
                    self.infected[s] = True
                    self.pq.put((s, 1))

            if t >= self.t + 1:
                self.pq.put((node, t - 1))
            else:
                self.infected.pop(node)

            #print(abs(infected_num - len(self.infected.keys())))
            if abs(infected_num - len(self.infected.keys())) < 2:
                return len(self.infected)

            count += 1

        return len(self.infected)

    def infect(self):
        r = random.uniform(0, 1)
        if r <= self.p:
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

        if not seed:
            seed = []
        print(self.infected.keys())
        not_seed = set(self.infected.keys()) - set(seed)
        not_infected = set(self.G.nodes()) - set(self.infected.keys()) - set(seed)

        nx.draw_networkx_nodes(self.G, pos, list(not_infected), alpha=0.2, node_size=20, node_color='grey')
        nx.draw_networkx_nodes(self.G, pos, list(not_seed), alpha=0.5, node_size=20, node_color='red', linewidths=0.)
        nx.draw_networkx_nodes(self.G, pos, seed, alpha=0.5, node_size=20, node_color='blue', linewidths=0.)
        nx.draw_networkx_edges(self.G, pos, alpha=0.2, node_size=0, width=0.1, edge_color='grey')

        plt.savefig(SISModel.get_data_dir() + SISModel.RESULT_DIR +
                    '_'.join([filename, str(self.p).replace('.',''), str(seed)]) , dpi=75, transparent=False)
        plt.close()
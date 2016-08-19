import networkx as nx
import matplotlib.pyplot as plt
import time
import epidemic

"""threshold model"""

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


class ThresholdModel(epidemic.OperaEpidemics):

    RESULT_DIR = '/data/threshold_model/'

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
        for i in xrange(len(seed_nodes)):
            self.marked[seed_nodes[i]] = True

        self.step = 1

    @timeit
    def spread(self):
        while True:
            current_step = self.marked.keys()
            count = 0
            while len(current_step):
                node = current_step.pop()
                neighbors = list(set(self.G.neighbors(node)))
                for i in xrange(len(neighbors)):
                    s = neighbors[i]
                    if s in self.marked:
                        continue
                    if self.vote(s):
                        self.marked[s] = True
                        count += 1
            if not count:
                break

            self.step += 1
            print(len(self.marked))

        return len(self.marked)

    def get_marked(self):
        return self.marked

    def vote(self, node):
        neighbors = self.G.neighbors(node)
        return float(len(set(neighbors).intersection(self.marked.keys()))) >= self.threshold * float(len(neighbors))

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
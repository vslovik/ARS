import networkx as nx
import threshold_model as tm

"""threshold model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"

thresholds = [float(i) / 100. for i in range(100)]

graph = tm.ThresholdModel.get_opera_graph()
seed = tm.ThresholdModel.get_hubs(graph, 10)
o_sizes = []
for i in xrange(len(thresholds)):
    o_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 16)
seed = tm.ThresholdModel.get_hubs(graph, 10)
ba_sizes = []
for i in xrange(len(thresholds)):
    ba_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.01)
seed = tm.ThresholdModel.get_hubs(graph, 100)
er_sizes = []
for i in xrange(len(thresholds)):
    er_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
print(er_sizes)

tm.ThresholdModel.plot_spread_size_distribution(thresholds, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
                                             tm.ThresholdModel.get_data_dir() + tm.ThresholdModel.RESULT_DIR + 'spread_size_distribution.png')
import networkx as nx
import sir_model as sm

"""SIR model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"

probabilities = [float(i)/100. for i in range(100)]
t = 1

graph = sm.SIRModel.get_opera_graph()
seed = sm.SIRModel.get_hubs(graph, 50)
o_sizes = []
for i in xrange(len(probabilities)):
    o_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 1)
seed = sm.SIRModel.get_hubs(graph, 50)
ba_sizes = []
for i in xrange(len(probabilities)):
    ba_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = sm.SIRModel.get_hubs(graph, 50)
er_sizes = []
for i in xrange(len(probabilities)):
    er_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
print(er_sizes)

sm.SIRModel.plot_spread_size_distribution(probabilities, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
                                          sm.SIRModel.get_data_dir() + sm.SIRModel.RESULT_DIR + 'spread_size_distribution.png')
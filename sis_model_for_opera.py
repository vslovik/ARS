import networkx as nx
import sis_model as sm

"""SIS model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"

probabilities = [float(i)/100. for i in range(100)]
t = 1

graph = sm.SISModel.get_opera_graph()
seed = sm.SISModel.get_random_seed(graph, 200)
print(seed)
o_sizes = []
for i in xrange(len(probabilities)):
    print(probabilities[i])
    o_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
print(o_sizes)

graph = nx.barabasi_albert_graph(4604, 10)
seed = sm.SISModel.get_random_seed(graph, 200)
ba_sizes = []
for i in xrange(len(probabilities)):
    ba_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = sm.SISModel.get_random_seed(graph, 200)
er_sizes = []
for i in xrange(len(probabilities)):
    er_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
print(er_sizes)

sm.SISModel.plot_spread_size_distribution(probabilities, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
                                       sm.SISModel.get_data_dir() + sm.SISModel.RESULT_DIR + 'spread_size_distribution.png')
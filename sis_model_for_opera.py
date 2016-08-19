import networkx as nx
import sis_model as sm

"""SIS model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"

stuttgart = [254, 399, 443, 578, 628, 858, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1050, 1102, 1343, 1380, 1440, 1551, 1552, 1569, 1601, 1821, 1843, 1957, 1958, 1959, 2052, 2055, 2063, 2135, 2136, 2157, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332, 2333, 2383, 2480, 2512, 2589, 2590, 2591, 2592, 2593, 2594, 2595, 2611, 2612, 2613, 2614, 2615, 2616, 2749, 2750, 2751, 2752, 2753, 2754, 3032, 3034, 3035, 3102, 3103, 3104, 3105, 3106, 3107, 3114, 3115, 3117, 3118, 3200, 3201, 3306, 3373, 3432, 3467, 3468, 3469, 3470, 3471, 3472, 3473, 3474, 3568, 3705, 3706, 3707, 3909, 3910, 3911, 3912, 3974, 4000, 4001, 4002, 4003, 4004, 4005, 4030, 4031, 4032, 4123, 4128, 4175, 4177, 4181, 4226, 4227, 4228, 4229, 4230, 4307, 4308, 4309, 4310, 4323, 4386, 4387, 4388, 4450, 4472, 4473, 4474, 4536, 4537, 4688, 4738, 4739, 4771]

probabilities = [float(i)/10. for i in range(2, 7)]
t = 1

# graph = sm.SISModel.get_opera_graph()
# seed = sm.SISModel.get_random_seed(graph, 100)
# #seed = stuttgart[0:100]
# print(seed)
# o_sizes = []
# for i in xrange(len(probabilities)):
#     print(probabilities[i])
#     o_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
# print(o_sizes)
#
# graph = nx.barabasi_albert_graph(4604, 10)
# seed = sm.SISModel.get_random_seed(graph, 100)
# ba_sizes = []
# for i in xrange(len(probabilities)):
#     ba_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
# print(ba_sizes)

graph = nx.erdos_renyi_graph(4604, 0.005)
seed = sm.SISModel.get_random_seed(graph, 100)
er_sizes = []
for i in xrange(len(probabilities)):
    er_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
print(er_sizes)

# sm.SISModel.plot_spread_size_distribution(probabilities, [o_sizes, ba_sizes, er_sizes], ['blue', 'black', 'red'],
#                                        sm.SISModel.get_data_dir() + sm.SISModel.RESULT_DIR + 'spread_size_distribution.png', 'p')
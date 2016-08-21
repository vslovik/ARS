import networkx as nx
import threshold_model as tm

"""threshold model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"

stuttgart = [254, 399, 443, 578, 628, 858, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1050,
             1102, 1343, 1380, 1440, 1551, 1552, 1569, 1601, 1821, 1843, 1957, 1958, 1959, 2052, 2055, 2063, 2135,
             2136, 2157, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332, 2333, 2383, 2480, 2512, 2589, 2590,
             2591, 2592, 2593, 2594, 2595, 2611, 2612, 2613, 2614, 2615, 2616, 2749, 2750, 2751, 2752, 2753, 2754,
             3032, 3034, 3035, 3102, 3103, 3104, 3105, 3106, 3107, 3114, 3115, 3117, 3118, 3200, 3201, 3306, 3373,
             3432, 3467, 3468, 3469, 3470, 3471, 3472, 3473, 3474, 3568, 3705, 3706, 3707, 3909, 3910, 3911, 3912,
             3974, 4000, 4001, 4002, 4003, 4004, 4005, 4030, 4031, 4032, 4123, 4128, 4175, 4177, 4181, 4226, 4227,
             4228, 4229, 4230, 4307, 4308, 4309, 4310, 4323, 4386, 4387, 4388, 4450, 4472, 4473, 4474, 4536, 4537,
             4688, 4738, 4739, 4771]

stuttgart_degree_sorted = [399, 578, 1042, 2052, 628, 1046, 2329, 2135, 2753, 1050, 2328, 2616, 2331, 1343, 3467,
                           1601, 858, 2591, 1552, 3306, 254, 2063, 3102, 443, 4123, 2512, 3107, 3471, 1038, 3106,
                           1569, 2611, 1440, 4128, 1551, 2157, 3911, 1380, 3104, 4181, 1821, 1843, 3912, 2383, 3115,
                           2324, 3910, 1036, 1102, 4177, 4227, 4001, 1958, 3035, 2136, 2332, 3974, 3032, 4175, 4308,
                           4310, 3568, 2594, 3118, 4688, 3034, 2752, 1040, 1041, 1043, 3705, 2754, 3373, 4032, 2055,
                           1045, 2480, 4323, 3468, 3469, 3470, 3472, 3473, 3474, 4386, 4387, 4388, 3432, 3114, 3117,
                           2750, 2589, 2590, 2595, 4226, 4228, 4229, 4230, 2333, 2592, 2593, 2325, 2326, 2327, 2330,
                           2749, 4309, 4307, 4738, 4739, 4472, 4473, 4474, 4002, 4003, 4004, 4000, 4005, 1037, 1044,
                           2612, 2613, 2614, 2615, 1039, 3706, 3707, 4771, 3105, 3103, 2751, 3200, 3201, 3909, 4536,
                           4537, 4030, 4031, 4450, 1957, 1959]


def get_avg_stuttgart_degree():
    graph = tm.ThresholdModel.get_opera_graph()
    degree = sorted(nx.degree(graph, nbunch=stuttgart).items(), key=lambda x: x[1], reverse=True)
    print(degree)
    print([node for (node, value) in degree])
    return (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))


def spread_size_distribution_vs_probability():

    thresholds = [float(i) / 100. for i in range(100)]
    graph = tm.ThresholdModel.get_opera_graph()
    seed = tm.ThresholdModel.get_hubs(graph, 100)
    o_sizes = []
    for i in xrange(len(thresholds)):
        o_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
    print(o_sizes)

    seed = stuttgart_degree_sorted[0:100]
    st_o_sizes = []
    for i in xrange(len(thresholds)):
        st_o_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
    print(st_o_sizes)

    graph = nx.barabasi_albert_graph(4604, 11)
    seed = tm.ThresholdModel.get_hubs(graph, 100)
    ba_sizes = []
    for i in xrange(len(thresholds)):
        ba_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
    print(ba_sizes)

    graph = nx.erdos_renyi_graph(4604, 0.0047)
    seed = tm.ThresholdModel.get_hubs(graph, 100)
    er_sizes = []
    for i in xrange(len(thresholds)):
        er_sizes.append(tm.ThresholdModel(graph, seed, thresholds[i]).spread())
    print(er_sizes)

    tm.ThresholdModel.plot_spread_size_distribution(
        thresholds,
        [o_sizes, ba_sizes, er_sizes, st_o_sizes],
        ['blue', 'black', 'red', 'orange'],
        tm.ThresholdModel.get_data_dir() + tm.ThresholdModel.RESULT_DIR + 'spread_size_distribution.png'
    )


def compare_two_spreads():
    graph = tm.ThresholdModel.get_opera_graph()
    seed = tm.ThresholdModel.get_hubs(graph, 100)
    st_seed = stuttgart_degree_sorted[0:100]
    threshold = 0.21
    model = tm.ThresholdModel(graph, seed, threshold)
    model.spread()
    model.draw('spread', seed)
    model = tm.ThresholdModel(graph, st_seed, threshold)
    model.spread()
    model.draw('spread_stuttgart', seed)

#spread_size_distribution_vs_probability()
compare_two_spreads()
print(get_avg_stuttgart_degree())
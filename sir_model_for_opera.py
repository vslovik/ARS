import networkx as nx
import sir_model as sm

"""SIR model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"


def spread_size_distribution_vs_probability():

    probabilities = [float(i)/100. for i in range(100)]
    t = 5

    graph = sm.SIRModel.get_opera_graph()
    seed = sm.SIRModel.get_hubs(graph, 100)
    o_sizes = []
    for i in xrange(len(probabilities)):
        o_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
    print(o_sizes)

    graph = nx.barabasi_albert_graph(4604, 11)
    seed = sm.SIRModel.get_hubs(graph, 100)
    ba_sizes = []
    for i in xrange(len(probabilities)):
        ba_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
    print(ba_sizes)

    graph = nx.erdos_renyi_graph(4604, 0.0047)
    seed = sm.SIRModel.get_hubs(graph, 100)
    er_sizes = []
    for i in xrange(len(probabilities)):
        er_sizes.append(sm.SIRModel(graph, seed, probabilities[i], t).spread())
    print(er_sizes)

    sm.SIRModel.plot_spread_size_distribution(
        probabilities,
        [o_sizes, ba_sizes, er_sizes],
        ['blue', 'black', 'red'],
        sm.SIRModel.get_data_dir() + sm.SIRModel.RESULT_DIR + 'spread_size_distribution.png',
        'p'
    )


def spread_size_distribution_vs_time():

    probabilities = [float(i) / 10. for i in range(2, 7)]

    graph = sm.SIRModel.get_opera_graph()
    seed = sm.SIRModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            print(probabilities[i])
            model = sm.SIRModel(graph, seed, probabilities[i], t, True)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        m = min(len(ts) for ts in time_series)
        sm.SIRModel.plot_spread_size_distribution(
            xrange(m),
            map(lambda x: x[0:m], time_series),
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SIRModel.get_data_dir()
            + sm.SIRModel.RESULT_DIR
            + 'o_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )

    graph = nx.barabasi_albert_graph(4604, 11)
    seed = sm.SIRModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            model = sm.SIRModel(graph, seed, probabilities[i], t, True)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        m = min(len(ts) for ts in time_series)
        sm.SIRModel.plot_spread_size_distribution(
            xrange(m),
            map(lambda x: x[0:m], time_series),
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SIRModel.get_data_dir()
            + sm.SIRModel.RESULT_DIR
            + 'ba_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )

    graph = nx.erdos_renyi_graph(4604, 0.0047)
    seed = sm.SIRModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            model = sm.SIRModel(graph, seed, probabilities[i], t, True)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        m = min(len(ts) for ts in time_series)
        sm.SIRModel.plot_spread_size_distribution(
            xrange(m),
            map(lambda x: x[0:m], time_series),
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SIRModel.get_data_dir()
            + sm.SIRModel.RESULT_DIR
            + 'er_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )


spread_size_distribution_vs_probability()
#spread_size_distribution_vs_time()
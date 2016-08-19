import networkx as nx
import sis_model as sm

"""SIS model on opera graph"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"


def spread_size_distribution_vs_probability():
    probabilities = [float(i) / 100. for i in range(100)]
    t = 5

    graph = sm.SISModel.get_opera_graph()
    seed = sm.SISModel.get_random_seed(graph, 100)
    print(seed)
    o_sizes = []
    for i in xrange(len(probabilities)):
        print(probabilities[i])
        o_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
    print(o_sizes)

    graph = nx.barabasi_albert_graph(4604, 10)
    seed = sm.SISModel.get_random_seed(graph, 100)
    ba_sizes = []
    for i in xrange(len(probabilities)):
        ba_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
    print(ba_sizes)

    graph = nx.erdos_renyi_graph(4604, 0.005)
    seed = sm.SISModel.get_random_seed(graph, 100)
    er_sizes = []
    for i in xrange(len(probabilities)):
        er_sizes.append(sm.SISModel(graph, seed, probabilities[i], t).spread())
    print(er_sizes)

    sm.SISModel.plot_spread_size_distribution(
        probabilities,
        [o_sizes, ba_sizes, er_sizes],
        ['blue', 'black', 'red'],
        sm.SISModel.get_data_dir() + sm.SISModel.RESULT_DIR + 'spread_size_distribution.png',
        'p'
    )


def spread_size_distribution_vs_time():

    probabilities = [float(i) / 10. for i in range(2, 7)]

    graph = sm.SISModel.get_opera_graph()
    seed = sm.SISModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            model = sm.SISModel(graph, seed, probabilities[i], t, True, 100)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        sm.SISModel.plot_spread_size_distribution(
            xrange(len(time_series[0])),
            time_series,
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SISModel.get_data_dir()
            + sm.SISModel.RESULT_DIR
            + 'o_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )

    graph = nx.barabasi_albert_graph(4604, 10)
    seed = sm.SISModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            model = sm.SISModel(graph, seed, probabilities[i], t, True, 100)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        sm.SISModel.plot_spread_size_distribution(
            xrange(len(time_series[0])),
            time_series,
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SISModel.get_data_dir()
            + sm.SISModel.RESULT_DIR
            + 'ba_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )

    graph = nx.erdos_renyi_graph(4604, 0.005)
    seed = sm.SISModel.get_random_seed(graph, 100)
    for t in [1, 5, 10]:
        time_series = []
        for i in xrange(len(probabilities)):
            model = sm.SISModel(graph, seed, probabilities[i], t, True, 100)
            model.spread()
            time_series.append(model.get_time_series())
        print(time_series)
        sm.SISModel.plot_spread_size_distribution(
            xrange(len(time_series[0])),
            time_series,
            ['blue', 'red', 'green', 'orange', 'black'],
            sm.SISModel.get_data_dir()
            + sm.SISModel.RESULT_DIR
            + 'er_spread_size_distribution_time_series_t{}.png'.format(str(t)),
            't, steps'
        )


spread_size_distribution_vs_probability()
spread_size_distribution_vs_time()

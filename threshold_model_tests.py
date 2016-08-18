import networkx as nx
import threshold_model as tm
import unittest


class TestThresholdModel(unittest.TestCase):

    def test_full_adoption(self):
        graph = nx.Graph()
        graph.add_edges_from([
                (1, 2),
                (2, 3),
                (1, 4),
                (1, 5),
                (4, 5),
                (4, 2),
                (4, 3),
                (3, 6),
                (4, 6),
                (5, 6)
            ])
        a = 3
        b = 2
        p = float(b) / float(a + b)
        initial_adopters = [1, 4]

        spread = tm.ThresholdModel(graph, initial_adopters, p).spread()
        self.assertEqual(spread, graph.number_of_nodes())

    def test_clusters_partial_adoption(self):
        graph = nx.Graph()
        graph.add_edges_from([
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 6),
            (6, 4),
            (4, 5),
            (6, 9),
            (9, 10),
            (10, 8),
            (8, 5),
            (4, 7),
            (5, 7),
            (8, 7),
            (10, 7),
            (9, 7),
            (8, 14),
            (10, 12),
            (9, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (11, 15),
            (12, 15),
            (12, 16),
            (13, 16),
            (13, 17),
            (14, 17),
            (15, 16),
            (16, 17)
            ])

        a = 3
        b = 2
        p = float(b) / float(a + b)
        initial_adopters = [7, 8]
        model = tm.ThresholdModel(graph, initial_adopters, p)
        spread = model.spread()
        marked = model.get_marked()
        self.assertEqual(spread, 7)
        self.assertEqual(set(marked), {4, 5, 6, 7, 8, 9, 10})

    def test_clusters_full_adoption(self):
        graph = nx.Graph()
        graph.add_edges_from([
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 6),
            (6, 4),
            (4, 5),
            (6, 9),
            (9, 10),
            (10, 8),
            (8, 5),
            (4, 7),
            (5, 7),
            (8, 7),
            (10, 7),
            (9, 7),
            (8, 14),
            (10, 12),
            (9, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (11, 15),
            (12, 15),
            (12, 16),
            (13, 16),
            (13, 17),
            (14, 17),
            (15, 16),
            (16, 17)
            ])

        a = 4
        b = 2
        p = float(b) / float(a + b)
        initial_adopters = [7, 8]
        spread = tm.ThresholdModel(graph, initial_adopters, p).spread()
        self.assertEqual(spread, graph.number_of_nodes())

suite = unittest.TestLoader().loadTestsFromTestCase(TestThresholdModel)
unittest.TextTestRunner(verbosity=2).run(suite)



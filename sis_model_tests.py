import networkx as nx
import sis_model as sm
import unittest


class TestSISModel(unittest.TestCase):

    def test_infected(self):
        graph = nx.Graph()
        graph.add_edges_from([
                (1, 2)
            ])
        p = 1
        initial_adopters = [1]
        t = 1

        model = sm.SISModel(graph, initial_adopters, p, t)
        model.spread()
        infected = model.get_infected()
        self.assertEqual(len(infected), 1)

    def test_infection_free(self):
        graph = nx.Graph()
        graph.add_edges_from([
                (1, 2)
            ])
        p = 0.5
        initial_adopters = [1]
        t = 1

        model = sm.SISModel(graph, initial_adopters, p, t)
        model.spread()
        infected = model.get_infected()
        self.assertEqual(len(infected), 0)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSISModel)
unittest.TextTestRunner(verbosity=2).run(suite)

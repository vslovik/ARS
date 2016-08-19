import networkx as nx
import sir_model as sm
import unittest


class TestSIRModel(unittest.TestCase):

    def tes_fully_touched(self):
        graph = nx.Graph()
        graph.add_edges_from([
                (1, 2),
                (2, 3),
                (3, 1)
            ])
        p = 1
        initial_adopters = [1]
        t = 1

        model = sm.SIRModel(graph, initial_adopters, p, t)
        spread = model.spread()
        model.get_infected()
        self.assertEqual(spread, 3)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSIRModel)
unittest.TextTestRunner(verbosity=2).run(suite)

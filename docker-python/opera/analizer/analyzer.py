import networkx as nx
import matplotlib.pyplot as plt

"""www.gbopera.it graph analyse"""

__author__ = "Valeriya Slovikovskaya <vslovik@gmail.com>"
__version__ = "0.1"
__package__ = "analyzer"


class Analyzer(object):

    def __init__(self, input_file, output_filename, title, weighted=False, bipartite=False):
        self.output_filename = output_filename
        self.title = title
        self.weighted = weighted
        self.bipartite = bipartite
        self.G = None
        self.L = None
        self.R = None
        if bipartite:
            self.create_bipartite_graph(input_file, weighted)
        else:
            self.create_graph(input_file, weighted)
        n = self.G.number_of_nodes()
        self.ER = nx.erdos_renyi_graph(n, 0.05)
        self.BA = nx.barabasi_albert_graph(n, 5)

    def create_graph(self, input_file, weighted):
        if weighted:
            self.G = nx.read_weighted_edgelist(
                input_file,
                delimiter=";",
                nodetype=str,
                encoding='utf-8'
            )
            self.G.remove_edges_from(self.G.selfloop_edges())
        else:
            self.G = nx.read_edgelist(
                input_file,
                delimiter=";",
                nodetype=str,
                create_using=nx.MultiGraph()
            )

    def create_bipartite_graph(self, input_file, weighted):
        if weighted:
            self.L = nx.Graph()
            self.R = nx.Graph()
            self.G = nx.Graph()
        else:
            self.L = nx.MultiGraph()
            self.R = nx.MultiGraph()
            self.G = nx.MultiGraph()
        with open(input_file, 'r') as lines:
            for line in lines:
                arr = line.split(';')
                if len(arr) > 1:
                    self.L.add_node(arr[0])
                    self.R.add_node(arr[1])
                    if weighted:
                        self.G.add_edge(arr[0], arr[1], weight=arr[2])
                    else:
                        self.G.add_edge(arr[0], arr[1])

    def inform(self):
        self.draw()
        self.degree_histogram(self.G, self.title, self.output_filename)

        inf = self.info(self.G)
        if nx.is_connected(self.G):
            inf += self.distances(self.G)
        inf += self.connectivity()

        fh = open('{0}.txt'.format(self.output_filename), "w")
        for line in inf:
            print(line)
            fh.write('{0}\n'.format(line))
        fh.close()

    def inform_sub_graph(self, graph, i, title='Connected component'):
        self.draw_sub_graph(graph, i, title)
        self.degree_histogram(graph, '{0}. {1} {2}'.format(self.title, title, i), '{0}_cc{1}'.format(self.output_filename, i))

        inf = self.info(graph)
        n = graph.number_of_nodes()
        er = nx.erdos_renyi_graph(n, 0.05)
        inf += self.info(er, 'ER')
        ba = nx.barabasi_albert_graph(n, 5)
        inf += self.info(ba, 'BA')

        inf += self.distances(graph, er, ba)

        if nx.is_connected(graph):
            inf += self.centrality(graph, i, title)

        fh = open('{0}_cc_{1}.txt'.format(self.output_filename, i), "w")
        for line in inf:
            print(line)
            fh.write('{0}\n'.format(line))
        fh.close()

    @staticmethod
    def info(graph, title=None):
        degree = sorted(nx.degree(graph).items(), key=lambda x: x[1], reverse=True)
        avg = (0.0 + sum(value for (node, value) in degree)) / (0.0 + len(degree))
        (max_node, max_value) = degree[0]
        (min_node, min_value) = degree[len(degree) - 1]
        inf = list()
        if not title:
            inf.append('Number of nodes: {0}'.format(nx.number_of_nodes(graph)))
            inf.append('Number of edges: {0}'.format(nx.number_of_edges(graph)))
            inf.append('Is connected: {0}'.format(nx.is_connected(graph)))
        if title:
            inf.append(title)
        inf.append('Degree:')
        inf.append('Avg: {0}'.format(round(avg, 4)))
        inf.append('Max: {1} ({0})'.format(max_node, max_value))
        inf.append('Min: {1} ({0})'.format(min_node, min_value))
        inf.append('Density: {}'.format(round(nx.density(graph), 4)))
        return inf

    @staticmethod
    def degree_histogram(graph, title, output_filename, show=False):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.loglog(nx.degree_histogram(graph),'b-',marker='o')

        n = graph.number_of_nodes()
        er = nx.erdos_renyi_graph(n, 0.05)
        ba = nx.barabasi_albert_graph(n, 5)

        plt.loglog(nx.degree_histogram(er), 'r-', marker='o')
        plt.loglog(nx.degree_histogram(ba), 'k-', marker='o')

        plt.text(0.5, 0.97,'{0}'.format(title),
             horizontalalignment='center',
             transform=plt.gca().transAxes)

        plt.text(0.5, 0.94,  "degree histogram",
             horizontalalignment='center',
             transform=plt.gca().transAxes)

        plt.xlabel("degree")
        plt.ylabel("rank")
        plt.savefig('{0}_degree_histogram.png'.format(output_filename), dpi=75, transparent=True)
        if show:
            plt.show()

    @staticmethod
    def distances(graph, er=None, ba=None):
        inf = list()
        inf.append('Center: \n')
        names = nx.center(graph)
        names.sort()
        for name in names:
            inf.append('{0}'.format(name.rstrip()))
        if er and ba:
            inf.append('Diameter: {0} (ER: {1}, BA: {2})\n'.format(nx.diameter(graph), nx.diameter(er), nx.diameter(ba)))
        else:
            inf.append('Diameter: {0}\n'.format(nx.diameter(graph)))
        inf.append('Periphery: \n')
        names = nx.periphery(graph)
        names.sort()
        for name in nx.periphery(graph):
            inf.append('{0}'.format(name.rstrip()))
        if er and ba:
            inf.append('Radius: {0} (ER: {1}, BA: {2})\n'.format(nx.radius(graph), nx.radius(er), nx.radius(ba)))
            inf.append('Average shortest path length: {0} (ER: {1}, BA: {2})\n'.format(
                nx.average_shortest_path_length(graph),
                nx.average_shortest_path_length(er),
                nx.average_shortest_path_length(ba)
            ))
        else:
            inf.append('Radius: {0}\n'.format(nx.radius(graph)))
            inf.append('Radius: {0}\n'.format(nx.average_shortest_path_length(graph)))
        return inf

    def connectivity(self):
        inf = list()
        inf.append('Connectivity:')
        inf.append('Connected: {0}'.format(nx.is_connected(self.G)))
        inf.append('Number of connected components: {0}'.format(nx.number_connected_components(self.G)))
        connected_components = list(nx.connected_component_subgraphs(self.G))
        i = 0
        for component in connected_components:
            inf.append('Connected component {0}'.format(i))
            Analyzer.distances(component)
            self.inform_sub_graph(component, i, 'Connected component')
            if self.weighted:
                inf.append('Average clustering: {0}'.format(nx.average_clustering(component)))
            i += 1
            break # only first component is interesting
        return inf

    def centrality(self, graph, i, title):
        inf = list()
        inf.append('Centrality: \n')
        bt = nx.betweenness_centrality(graph)
        bt_sorted = sorted(bt.items(), key=lambda x: x[1], reverse=True)
        ego = False
        for (node, betweenness) in bt_sorted:
            if not ego:
                self.draw_sub_graph(nx.ego_graph(graph, node), i,
                                    '{0}. Ego graph for node {1}'.format(title, node), False, 'centrality_')
                ego = True
            inf.append('{0}, {1}'.format(node, betweenness))
        return inf

    def draw(self, show=False):
        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        if self.bipartite:
            nx.draw_networkx_nodes(self.L, pos, node_color='b', alpha=0.5, node_size=20)
            nx.draw_networkx_nodes(self.R, pos, node_color='r', alpha=0.5, node_size=20)
            nx.draw_networkx_edges(self.G, pos, alpha=0.5, node_size=0, width=0.2, edge_color='k')
        else:
            nx.draw_networkx_nodes(self.G, pos, node_color='b', alpha=0.5, node_size=20)
            nx.draw_networkx_edges(self.G, pos, alpha=0.5, node_size=0, width=0.1, edge_color='k')

        plt.title(self.title, fontdict={'color': 'k', 'fontsize': 22})
        plt.savefig(self.output_filename, dpi=75, transparent=True)

        if show:
            plt.show()

    def draw_sub_graph(self, graph, i=None, subtitle=None, show=False, file_prefix=''):
        try:
            pos = nx.nx_agraph.graphviz_layout(graph)
        except:
            pos = nx.spring_layout(graph, iterations=20)

        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        nx.draw_networkx_nodes(graph, pos, node_color='b', alpha=0.5, node_size=20)

        if self.bipartite:
            red = nx.Graph()
            for node in graph.nodes():
                if self.R.has_node(node):
                    red.add_node(node)
            nx.draw_networkx_nodes(red, pos, node_color='r', alpha=0.5, node_size=20)
            if red.number_of_nodes() < 16:
                nx.draw_networkx_labels(red, pos)

        nx.draw_networkx_edges(graph, pos, alpha=0.5, node_size=0, width=0.1, edge_color='k')

        plt.title('{0} {1} of {2}'.format(subtitle, i, self.title), fontdict={'color': 'k', 'fontsize': 14})

        plt.savefig('{0}{1}_cc{2}.png'.format(file_prefix, self.output_filename, i), dpi=75, transparent=True)

        if show:
            plt.show()
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import os


class CliqueSpy(object):

    SINGER_GRAPH_FILE = '/data/singer_singer/weighted/SINGER_SINGER.csv'
    SINGER_DICT = '/data/singer_singer/weighted/SINGER_DICT.csv'

    def __init__(self):
        self.G = nx.read_weighted_edgelist(
            CliqueSpy.get_data_dir() + CliqueSpy.SINGER_GRAPH_FILE,
            delimiter=';',
            encoding='utf-8'
        )
        self.G.remove_edges_from(self.G.selfloop_edges())
        self.singer_dict = CliqueSpy.read_dict(CliqueSpy.get_data_dir() + CliqueSpy.SINGER_DICT)

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/../..'

    def spy(self):
        k = 31 # k =1 => 5399
        cliques = list(c for c in nx.find_cliques(self.G) if len(c) >= k)
        print(cliques)
        print(len(cliques))

        for i in xrange(len(cliques)):
            filename = CliqueSpy.get_data_dir() + '/data/cliques/clique_{}'.format(i)
            self.write_partition(cliques[i], filename)
        print(str(len(cliques)) + '\n')

    def ego(self):
        bt = nx.betweenness_centrality(self.G)
        i = 0
        egos = dict()
        for (node, betweenness) in sorted(bt.items(), key=lambda x: x[1], reverse=True):
            print(node)
            nodes = nx.ego_graph(self.G, node).nodes()
            if len(nodes) > 90:
                egos[node] = nodes
                node_words = self.singer_dict[int(node)].split('|')
                filename = CliqueSpy.get_data_dir() + '/data/cliques/ego_{}_{}'.format(i, node_words[0])
                self.write_partition(nodes, filename)
                i += 1
                if i > 8:
                    break

        filename = CliqueSpy.get_data_dir() + '/data/cliques/egos'
        self.draw_partition(egos, filename)

    def draw_partition(self, egos, filename):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        colors = ['blue', 'yellow', 'green', 'red', 'orange', 'brown', 'black', 'cyan']
        i = 0
        for node in egos:
            nodes = egos[node]
            color = 'grey'
            if i < len(colors):
                color = colors[i]
            self.draw_ego(node, nodes, color)
            i += 1

        plt.savefig(filename, dpi=75, transparent=False)
        plt.close()

    def draw_ego(self, node, list_nodes, color):
        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        nx.draw_networkx_nodes(self.G, pos, list_nodes,
                               alpha=0.5, node_size=20, node_color=color)

        nx.draw_networkx_nodes(self.G, pos, [node],
                               alpha=0.5, node_size=60, node_color=color)

        list_edges = [(u, v) for (u, v) in self.G.edges()
                      if u in list_nodes and v in list_nodes]
        nx.draw_networkx_edges(self.G, pos, list_edges,
                               alpha=0.5, node_size=0, width=0.1, edge_color=color)

    @staticmethod
    def read_dict(dictionary_file):
        d = dict()
        fh = open(dictionary_file)
        for line in fh:
            items = line.split('|')
            d[int(items[0])] = '|'.join(items[1:])
        return d

    def write_partition(self, nodes, filename=''):
        tags = dict()

        ofh = open('{0}.txt'.format(filename), "w+")
        for item in nodes:
            item = int(item)
            if item in self.singer_dict:
                for t in self.singer_dict[int(item)].strip('\n').split('|'):
                    if t != '-':
                        if t in tags:
                            tags[t] +=1
                        else:
                            tags[t] = 1
                ofh.write(self.singer_dict[int(item)])
            else:
                print(item)
        i = 0
        for t in sorted(tags, key=tags.get, reverse=True):
            if tags[t] > 10:
                ofh.write('|'.join(['tag', t, str(tags[t])]) + '\n')
                i += 1
            if i > 100:
                break
        ofh.close()


CliqueSpy().ego()
import community
import networkx as nx
import matplotlib.pyplot as plt
import os


class CommunitySpy(object):

    SINGER_GRAPH_FILE = '/data/singer_singer/weighted/SINGER_SINGER.csv'
    SINGER_DICT = '/data/singer_singer/weighted/SINGER_DICT.csv'

    def __init__(self):
        self.G = nx.read_weighted_edgelist(
            CommunitySpy.get_data_dir() + CommunitySpy.SINGER_GRAPH_FILE,
            delimiter=';',
            encoding='utf-8'
        )
        self.G.remove_edges_from(self.G.selfloop_edges())
        self.singer_dict = CommunitySpy.read_dict(CommunitySpy.get_data_dir() + CommunitySpy.SINGER_DICT)

    @staticmethod
    def get_data_dir():
        return os.getcwd() + '/..'

    def get_best_partition(self):
        best_partition = community.best_partition(self.G)
        modlularity = community.modularity(best_partition, self.G)
        return modlularity, best_partition

    def get_partition_levels(self):
        dendrogram = community.generate_dendrogram(self.G)
        levels_num = len(dendrogram)

        levels = dict()
        for i in range(len(dendrogram)):
            levels[i] = community.partition_at_level(dendrogram, i)
        return levels_num, levels

    def spy(self):
        modlularity, best_partition = self.get_best_partition()
        print('Modularity: ' + str(modlularity))  # 0.629022183635

        size = len(set(best_partition.values()))
        print('Communities number: ' + str(size)) # 81

        levels_num, levels = self.get_partition_levels()
        print('Levels number: ' + str(levels_num)) #3

        # filter communities
        community_size_filters = [30, 120, 240]
        communities = dict()
        for level in xrange(0, levels_num):
            communities[level] = []
            size_filter = 30
            if level < len(community_size_filters):
                size_filter = community_size_filters[level]
            for community in xrange(0, size):
                print('Community number of level {}: {}'.format(level, len(set(levels[level].values()))))
                nodes = [nodes for nodes in levels[level].keys() if levels[level][nodes] == community]
                if len(nodes) > size_filter:
                    communities[level].append(nodes)

        for level in communities:
            count = 0
            for nodes in communities[level]:
                filename = CommunitySpy.get_data_dir() + '/data/communities/level_{}_{}'.format(level, count)
                self.write_partition(nodes, filename)
                count += 1
            filename = CommunitySpy.get_data_dir() + '/data/communities/level_{}'.format(level)
            self.draw_partition(communities[level], filename)

    def draw_partition(self, communities, filename):
        plt.rcParams['text.usetex'] = False
        plt.figure(figsize=(20, 20))
        plt.axis('off')

        colors = ['yellow', 'blue', 'green', 'red', 'orange', 'brown', 'black']
        for i in xrange(len(communities)):
            nodes = communities[i]
            color = 'grey'
            if i < len(colors):
                color = colors[i]
            self.draw_community(nodes, color)

        plt.savefig(filename, dpi=75, transparent=False)
        plt.close()

    def draw_community(self, list_nodes, color):
        try:
            pos = nx.nx_agraph.graphviz_layout(self.G)
        except:
            pos = nx.spring_layout(self.G, iterations=20)

        nx.draw_networkx_nodes(self.G, pos, list_nodes,
                               alpha=0.5, node_size=20, node_color=color)
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
        ofh = open('{0}.txt'.format(filename), "w")
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


CommunitySpy().spy()

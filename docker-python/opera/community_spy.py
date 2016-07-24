import community
import networkx as nx
import matplotlib.pyplot as plt
from analizer import analyzer


def draw_partition(graph, partition, community_num=None, filename='', title='Opera singers connection graph, GBOPERA, 2008-2016', ):
    try:
        pos = nx.nx_agraph.graphviz_layout(graph)
    except:
        pos = nx.spring_layout(graph, iterations=20)

    plt.rcParams['text.usetex'] = False
    plt.figure(figsize=(20, 20))
    plt.axis('off')

    size = len(set(partition.values()))
    count = 0.
    for com in set(partition.values()) :
        if community_num is not None and com != community_num and community_num < size:
            continue
        count += 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(graph, pos, list_nodes, alpha=0.5, node_size=20,
                                    node_color=str(count / float(size)))
        if len(list_nodes) > 1:
            list_edges = [(u, v) for (u, v) in graph.edges()
                      if u in list_nodes and v in list_nodes]

            nx.draw_networkx_edges(graph, pos, list_edges, alpha=0.5, node_size=0, width=0.1, edge_color='k')

        if community_num is not None and com == community_num and community_num < size:
            break
        break

    plt.title(title, fontdict={'color': 'k', 'fontsize': 22})
    plt.savefig(filename, dpi=75, transparent=False)
    plt.close()


def write_partition(graph, partition, community_num=None, filename=''):
    size = len(set(partition.values()))
    count = 0.
    for com in set(partition.values()) :
        if community_num is not None and com != community_num and community_num < size:
            continue
        count += 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        fh = open('{0}.txt'.format(filename), "w")
        fh.write(str(len(list_nodes)))
        fh.write(str(list_nodes))
        fh.close()
        if community_num is not None and com == community_num and community_num < size:
            break


G = analyzer.Analyzer(
    "../data/singer_singer/multi/singer_singer.csv",
    "",
    "",
    True).get_graph()

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
#G = nx.erdos_renyi_graph(30, 0.05)

best_partition = community.best_partition(G)
m = community.modularity(best_partition, G)
print('modularity' + str(m)) # 0.601893866813
size = len(set(best_partition.values()))
print('communities number: ' + str(size))
for i in xrange(0, size):
    draw_partition(G, best_partition, i, 'best_' + str(i))
    write_partition(G, best_partition, i, 'best_' + str(i))

dendrogram = community.generate_dendrogram(G)
levels_num = len(dendrogram)
print(levels_num)

for i in xrange(0, levels_num):
    partition_level = community.partition_at_level(dendrogram, i)
    draw_partition(G, partition_level, i, 'level_' + str(i))
    write_partition(G, partition_level, i, 'level_' + str(i))
for level in range(len(dendrogram) - 1) :
    print("partition at level", level, "is", community.partition_at_level(dendrogram, level))


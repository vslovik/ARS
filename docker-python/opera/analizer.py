import networkx as nx
G = nx.read_edgelist("/home/valerya/project/ars/ARS/docker-python/data/res.csv", delimiter=",", data=[("weight", int)])
G.edges(data=True)
edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )
pos = nx.random_layout(G)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
import matplotlib.pyplot as plt; plt.show()
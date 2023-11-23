import networkx as nx
import matplotlib.pyplot as plt

edges = []

edges.append(('U1', '1', {"junction_values" : [0,0]}))

G = nx.DiGraph(edges)

pos = nx.kamada_kawai_layout(G)

# edge_labels = {}
# for u, v, data in G.edges(data=True):
#     edge_labels[u, v] = data

# nx.draw_networkx_nodes(G, pos)
# nx.draw_networkx_edges(G, pos, connectionstyle="arc3,rad=0.1")
nx.draw(G, with_labels = True, node_color='r', edge_color='b')



plt.savefig("img/img.jpg")
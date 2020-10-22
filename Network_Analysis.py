import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


G = nx.read_gml('power.gml', label = 'id')

G.number_of_nodes()
G.number_of_edges()


### Nodes of highest degree



sorted(G.degree, key=lambda x: x[1], reverse=True)[:20]


### Degree Distribution


### Nodes of higher betweenness

G.betweenness = nx.betweenness_centrality(G)
G_betweenness = G.betweenness.items()
sorted(G_betweenness, key=lambda x: x[1], reverse=True)[:10]


### Edges of higher betweenness

G.edge_betweenness = nx.edge_betweenness_centrality(G)
G_edge_betweenness = G_edge_betweenness.items()
sorted(G_edge_betweenness, key=lambda x: x[1], reverse=True)[:10]


### Nodes of higher pagerank


G.pagerank = nx.pagerank(G)
G_pagerank = G.pagerank.items()
sorted(G_pagerank, key=lambda x: x[1], reverse=True)[:10]


### Clustering coefficient

nx.average_clustering(G)


### Closeness

G.closeness = nx.closeness_centrality(G)
G_closeness = G.closeness.items()
sorted(G_closeness, key=lambda x: x[1], reverse=True)[:10]

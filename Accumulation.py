import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
import ReadTSV
import Network_Analysis as NA
### Importing the graph


G=ReadTSV.data_to_digraph('body.tsv')
GG=NA.degree_cut(G,3000)

l,lp,ln=NA.edge_evaluation(GG)
NA.GraphDraw(GG,-1)
GGG=NA.DiGraphToGraph(GG,ln)
NA.GraphDraw(GGG)


GGGG=NA.SingleSignEdgesOnly(GG,-1)
NA.GraphDraw(GG,-1)
NA.GraphDraw(GGGG,-1)


_,l1,l2=NA.edge_evaluation(G)
weight={i:l1[i]-l2[i] for i in l1}
GGG=NA.MultigraphToGraph(G,weight)



l=NA.positive_negative_scores(GG)




### Basic stuff

G.number_of_nodes()
G.number_of_edges()


### Nodes of highest degree



sorted(G.degree, key=lambda x: x[1], reverse=True)[:20]


### Degree Distribution

degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color="b")

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)
plt.show()


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

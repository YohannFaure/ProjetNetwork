#!/usr/bin/env python3
"""
This is an example of usage of ProjectNetwork to plot the communities inside the Reddit dataset
"""

# Modules
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
import ReadTSV
import Network_Analysis as NA
import Community_Detection as CD

### Importing the graph

# The data has to be downloaded here : http://snap.stanford.edu/data/soc-RedditHyperlinks.html
G=ReadTSV.data_to_digraph('body.tsv')

GG=NA.degree_cut(G,150)
_,l1,l2=NA.edge_evaluation(GG)
weight={i:l1[i] for i in l1}
GGG=NA.DiGraphToGraph(NA.MultigraphToGraph(GG,l1))
partition = CD.plot_community(GGG,comscale=15.,nodscale=3.)


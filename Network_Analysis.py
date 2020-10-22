#!/usr/bin/env python
# coding: utf-8

# In[3]:


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# In[12]:


G = nx.read_edgelist("C:/Users/Flora/Desktop/M2 Systèmes Complexes/Complex Networks/Tutorial_1/airportData.edges")


# In[13]:


G.number_of_nodes()


# In[14]:


G.number_of_edges()


# ## Nodes of highest degree

# In[15]:


sorted(G.degree, key=lambda x: x[1], reverse=True)[:20]


# ## Degree Distribution

# In[ ]:





# ## Nodes of higher betweenness

# In[16]:


G.betweenness = nx.betweenness_centrality(G)
G_betweenness = G.betweenness.items()
sorted(G_betweenness, key=lambda x: x[1], reverse=True)[:10]


# ## Edges of higher betweenness

# In[ ]:


G.edge_betweenness = nx.edge_betweenness_centrality(G)
G_edge_betweenness = G_edge_betweenness.items()
sorted(G_edge_betweenness, key=lambda x: x[1], reverse=True)[:10]


# ## Nodes of higher pagerank

# In[ ]:


G.pagerank = nx.pagerank(G)
G_pagerank = G.pagerank.items()
sorted(G_pagerank, key=lambda x: x[1], reverse=True)[:10]


# ## Clustering coefficient

# In[ ]:


nx.average_clustering(G)


# ## Closeness

# In[ ]:


G.closeness = nx.closeness_centrality(G)
G_closeness = G.closeness.items()
sorted(G_closeness, key=lambda x: x[1], reverse=True)[:10]


# In[ ]:





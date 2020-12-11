#!/usr/bin/env python3
"""
This document is designed to study communities in networks.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def community_layout(g, partition,comscale=8.,nodscale=3.):
    """
    Compute the layout for a modular graph.

    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions

    comscale -- positive float, ~10, representing the inverse of the
        spring constant between communities

    nodscale -- positive float, ~3, representing the inverse of the
        spring constant between nodes

    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions
    """
    pos_communities = _position_communities(g, partition, scale=comscale)
    pos_nodes = _position_nodes(g, partition, scale=nodscale)
    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]
    return(pos)

def _position_communities(g, partition, **kwargs):
    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)
    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))
    # find layout for communities
    pos_communities = nx.spring_layout(hypergraph, **kwargs)
    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]
    return(pos)

def _find_between_community_edges(g, partition):
    edges = dict()
    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]
        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]
    return(edges)

def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """
    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]
    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph, **kwargs)
        pos.update(pos_subgraph)
    return(pos)

def plot_community(g,comscale=8.,nodscale=3.):
    # to install networkx 2.0 compatible version of python-louvain use:
    # pip install -U git+https://github.com/taynaud/python-louvain.git@networkx2
    from community import community_louvain
    partition = community_louvain.best_partition(g)
    pos = community_layout(g, partition,comscale=comscale,nodscale=nodscale)
    d = dict(g.degree)
    allcolors = ['r','g','cyan','orange','yellow','pink','lime','chartreuse','deepskyblue','olive','salmon','tomato','chocolate','bisque','palegreen','royalblue','springgreen']
    colors = list(partition.values())
    for i in range(len(colors)):
        colors[i]=allcolors[colors[i]%len(allcolors)]
    nx.draw(g, pos, node_color=colors,node_size=[v * 10 for v in d.values()],edgelist=[])
    #nx.draw_networkx_edges(g, pos, edgelist=None, width=1.0, edge_color='k', style='solid', alpha=.1, arrowstyle='-|>', arrowsize=10)
    #nx.draw_networkx_labels(g, pos, labels=None, font_size=13, font_color='r', font_family='calibri')
    for node, (x, y) in pos.items():
        plt.text(x, y, node, fontsize=8, ha='center', va='center')
    plt.show()
    return(partition)

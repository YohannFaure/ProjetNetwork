import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

def degree_distribution(G):
    """
    """
    degrees = sorted([(d,n) for n, d in G.degree()], reverse=True)  # degree sequence
    return(degrees)

def Degree_distribution_plot(G):
    """
    """
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
    return(None)


def degree_cut(G,mindeg,degrees=None):
    GG=G.copy
    if not degrees:
        degrees = degree_distribution(GG)
    i=0
    while degrees[i][0]>mindeg:
        i+=1
    GG.remove_nodes_from([degrees[j][1] for j in range(i,len(degrees))])
    return(GG)

def GraphDraw(G):


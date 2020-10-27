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
    return(None)

def clustering_coefficient(G):
    G_clustering = nx.clustering(G)
    G_clustering = G_clustering.items()
    nodes_by_clustering_coefficient = [t[0] for t in sorted(G_clustering, key=lambda x: x[1], reverse=True)]
    clustering_coefficients = [t[1] for t in sorted(G_clustering, key=lambda x: x[1], reverse=True)]
    return(nodes_by_clustering_coefficient, clustering_coefficients)


def total_communities_scores(G):
    '''
    Computes the total score of each community (node) whithin the graph, where each positive
    link to a given community increases its score by one,
    and each negative link decreases its score by one
    '''
    emetteurs = np.array(G.edges())[:,0] #list of communities posting about another
    receveurs = np.array(G.edges())[:,1] #list of communities being judged
    receveurs_score = np.zeros(G.number_of_nodes())
    for edge_number in range(G.number_of_edges()):
            #getting the edge data of (node x, node y) in the form of a dictionary
            edge_data = G.get_edge_data(emetteurs[edge_number], receveurs[edge_number])
            #getting the info on whether the interaction was positive or negative (+1/-1)
            edge_label = edge_data['POST_LABEL']
            receveurs_score[receveurs[edge_number]] += edge_label
    return(receveurs_score)


def positive_negative_scores(G):
    '''
    Returns the total number of positive interactions for each communitiy (node)
    and the total number of negative interactions for each community in the form of two lists.
    '''    
    emetteurs = np.array(G.edges())[:,0] #list of communities posting about another
    receveurs = np.array(G.edges())[:,1] #list of communities being judged
    receveurs_score_positif = np.zeros(G.number_of_nodes())
    receveurs_score_negatif = np.zeros(G.number_of_nodes())
    for edge_number in range(G.number_of_edges()):
        #getting the edge data of (node x, node y) in the form of a dictionary
        edge_data = G.get_edge_data(emetteurs[edge_number], receveurs[edge_number])
        #getting the info on whether the interaction was positive or negative (+1/-1)
        edge_label = edge_data['POST_LABEL']
        if edge_label == 1:
            receveurs_score_positif[receveurs[edge_number]] += 1
        elif edge_label == -1:
            receveurs_score_negatif[receveurs[edge_number]] += 1
        else:
            print('Edge label not equal to -1 or 1. Edge label for edge number ', edge_number, ' is ', edge_label)
    return(receveurs_score_positif, receveurs_score_negatif)

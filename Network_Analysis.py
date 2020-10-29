import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

def degree_distribution(G):
    """
    returns the sorted degree list of a graph.
    """
    degrees = sorted([(d,n) for n, d in G.degree()], reverse=True)  # degree sequence
    return(degrees)

def Degree_distribution_plot(G):
    """
    Plots the degree distribution of a graph.
    """
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    #fig, ax = plt.subplots()
    plt.scatter(deg, cnt, marker="+")
    plt.title("Degree Distribution")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.xscale('log')
    plt.yscale('log')
    #ax.set_xticks([d + 0.4 for d in deg])
    #ax.set_xticklabels(deg)
    plt.show()
    return(None)

def degree_cut(G,mindeg,degrees=None):
    """
    takes a graph G and returns a degree cutted graph, with minimum degree mindeg.
    You can supply your own degree dictionnary.
    """
    GG=G.copy()
    if not degrees:
        degrees = degree_distribution(GG)
    i=0
    while degrees[i][0]>mindeg:
        i+=1
    GG.remove_nodes_from([degrees[j][1] for j in range(i,len(degrees))])
    return(GG)


def edge_evaluation(GG):
    """
    Evaluates the edge_label needed for GraphDraw.
    It can also be used to compute the positive and negative weight of every edge.
    Input : Multi(Di)Graph
    Output : 3 dictionaries, one containing the sum of all jugements,
        a positive only, and a negative only.
    """
    # Define the three dict
    edge_labels={}
    edge_labels_posit={}
    edge_labels_negat={}
    for edge in GG.edges():
        e0=edge[0]
        e1=edge[1]
        # if not visited yet
        if not edge in edge_labels:
            edge_labels[edge]=0
            edge_labels_posit[edge]=0
            edge_labels_negat[edge]=0
            # get_edge_data gives a dictionnary with keys {0,...,n}
            # with n the multiplicity of the edge.
            dicdata=GG.get_edge_data(e0,e1)
            for i in dicdata:
                data=dicdata[i]
                edge_labels[edge] += data['POST_LABEL']
                if data['POST_LABEL'] == 1:
                    edge_labels_posit[edge]+=1
                else :
                    edge_labels_negat[edge]-=1
    return(edge_labels,edge_labels_posit,edge_labels_negat)

def GraphDraw(GG,label_type=0):
    """
    Draws a Graph. Checks wether it's a directed graph or a simple graph before.
    label_type corresponds to wether you want the total score of every edge (0)
    the positive score only (1), or the negative score (-1)
    """
    # Define
    pos = nx.circular_layout(GG)
    plt.figure()    
    nx.draw(GG,pos,edge_color='black',width=1,linewidths=1,
        node_size=1000,node_color='pink',alpha=0.8,
        labels={node:node for node in GG.nodes()})
    if type(GG)==nx.classes.multidigraph.MultiDiGraph or type(GG)==nx.classes.multidigraph.MultiGraph :
        edge_labels=edge_evaluation(GG)[label_type]
    else:
        edge_labels = {edge:GG.get_edge_data(edge[0],edge[1])['POST_LABEL']
            for edge in GG.edges()}    
    nx.draw_networkx_edge_labels(GG,pos, edge_labels=edge_labels,font_color='red',label_pos=.2)
    plt.axis('off')
    plt.show()
    return(None)



def MultigraphToGraph(G,weight=None):
    """
    Converts a Multi(Di)Graph into a (Di)Graph.
    """
    if type(G)==nx.classes.multidigraph.MultiDiGraph :
        GG = nx.DiGraph()
    elif type(G)==nx.classes.multidigraph.MultiGraph :
        GG = nx.Graph()
    else:
        raise Exception("Not suported data type : {}".format(type(GG)))
    for u,v in G.edges():
        if not weight:
            w=1
        else:
            w = weight[(u,v)]
        if GG.has_edge(u,v):
            GG[u][v]['weight'] += w
        else:
            GG.add_edge(u, v, weight=w)
    return(GG)


def dict_to_sorted_lists(di,j=1):
    sorted_di = sorted(di.items(), key=lambda x: x[j],reverse=True)
    return(sorted_di)

def clustering_coefficient_lists(G):
    """
    Computes the clustering coefficient of every , on Graphs, not Multigraphs.
    """
    G_clustering = nx.clustering(G)
    list_clust=dict_to_sorted_lists(G_clustering)
    return([a[0] for a in list_clust],[a[1] for a in list_clust])

def total_communities_scores(G):
    '''
    Computes the total score of each community (node) whithin the graph, where each positive
    link to a given community increases its score by one,
    and each negative link decreases its score by one
    '''
    emetteurs = np.array(G.edges)[:,0] #list of communities posting about another
    receveurs = np.array(G.edges)[:,1] #list of communities being judged
    receveurs_score = dict.fromkeys(G.nodes(), 0)
    for edge_number in range(G.number_of_edges()):
            #getting the edge data of (node x, node y) in the form of a dictionary
            edge_data = G.get_edge_data(emetteurs[edge_number], receveurs[edge_number])[0]
            #getting the info on whether the interaction was positive or negative (+1/-1)
            edge_label = edge_data['POST_LABEL']
            receveurs_score[receveurs[edge_number]] += edge_label
    return(receveurs_score)


def positive_negative_scores(G):
    '''
    Returns the total number of positive interactions for each communitiy (node)
    and the total number of negative interactions for each community in the form of two lists.
    '''
    emetteurs = np.array(G.edges)[:,0] #list of communities posting about another
    receveurs = np.array(G.edges)[:,1] #list of communities being judged
    positive_score = dict.fromkeys(G.nodes(), 0)
    negative_score = dict.fromkeys(G.nodes(), 0)
    for edge_number in range(G.number_of_edges()):
        #getting the edge data of (node x, node y) in the form of a dictionary
        edge_data = G.get_edge_data(emetteurs[edge_number], receveurs[edge_number])[0]
        #getting the info on whether the interaction was positive or negative (+1/-1)
        edge_label = edge_data['POST_LABEL']
        if edge_label == 1:
            positive_score[receveurs[edge_number]] += 1
        elif edge_label == -1:
            negative_score[receveurs[edge_number]] += 1
        else:
            print('Edge label not equal to -1 or 1. Edge label for edge number ', edge_number, ' is ', edge_label)
    return(positive_score, negative_score)

#!/usr/bin/env python3
"""
This document is designed to study the data from
    http://snap.stanford.edu/data/soc-RedditHyperlinks.html
and imported with
    ReadTSV.py
It contains functions that can easilly be adapted to any Multi(Di)Graph treatment in networkx.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections
from re import match
import datetime

def degree_distribution(G):
    """
    returns the sorted degree list of a graph.
    """
    degrees = sorted([(d,n) for n, d in G.degree()], reverse=True)  # degree sequence
    return(degrees)

def Degree_distribution_plot(G,show=True):
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
    plt.grid(which='both')
    #ax.set_xticks([d + 0.4 for d in deg])
    #ax.set_xticklabels(deg)
    if show:
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
    if type(GG)==nx.classes.multidigraph.MultiDiGraph or type(GG)==nx.classes.multigraph.MultiGraph :
        edge_labels=edge_evaluation(GG)[label_type]
    else:
        try:
            edge_labels = {edge:GG.get_edge_data(edge[0],edge[1])['POST_LABEL']
             for edge in GG.edges()}
        except KeyError:
            edge_labels = {edge:GG.get_edge_data(edge[0],edge[1])['weight']
             for edge in GG.edges()}
        except:
            edge_labels = {edge:1 for edge in GG.edges()}
    nx.draw_networkx_edge_labels(GG,pos, edge_labels=edge_labels,font_color='red',label_pos=.3)
    plt.axis('off')
    plt.show()
    return(None)



def MultigraphToGraph(G,weight=None):
    """
    Converts a Multi(Di)Graph into a (Di)Graph.
    weight is a dictionnary supposed to hold each new edge only once as a key.
    """
    if type(G)==nx.classes.multidigraph.MultiDiGraph :
        GG = nx.DiGraph()
    elif type(G)==nx.classes.multigraph.MultiGraph :
        GG = nx.Graph()
    else:
        raise Exception("Not suported data type : {}".format(type(GG)))
    for u,v in G.edges():
        if not weight:
            w=1
        else:
            w = weight[(u,v)]
        if not GG.has_edge(u,v):
            GG.add_edge(u, v, weight=w)
    return(GG)

def DiGraphToGraph(G,weight=None):
    """
    converts a (multiple) Directed graph into a normal graph
    """
    if type(G)!=nx.classes.digraph.DiGraph and type(G)!=nx.classes.multidigraph.MultiDiGraph :
        raise Exception("Not suported data type : {}".format(type(GG)))
    GG = nx.Graph()
    for u,v in G.edges():
        if not GG.has_edge(u,v):
            if not weight:
                w=1
            else:
                try:
                    w = weight[(u,v)]+weight[(v,u)]
                except:
                    w = weight[(u,v)]
            GG.add_edge(u, v, weight=w)
    return(GG)

def SingleSignEdgesOnly(G,sign=1):
    """
    Takes a Multi(di)Graph as input.
    Returns a Multi(di)Graph with only the positive (resp. negative) edges, if sign = 1 (resp. -1).
    """
    GG=nx.classes.multidigraph.MultiDiGraph()
    if sign not in [-1,1]:
        raise Exception("Bad sign argument : {}".format(sign))
    Edges_Dict = nx.get_edge_attributes(G,'POST_LABEL')
    for e in Edges_Dict:
        if Edges_Dict[e]==sign:
            GG.add_edge(e[0],e[1],POST_LABEL=1)
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



def total_communities_scores_emitter(G):
    '''
    Computes the total emitting score of each community (node) whithin the graph, where each positive
    link to a another community from a given community increases its score by one,
    and each negative link decreases its score by one
    '''
    emitters = np.array(G.edges)[:,0] #list of communities posting about another
    receivers = np.array(G.edges)[:,1] #list of communities being judged
    emitter_score = dict.fromkeys(G.nodes(), 0)
    for edge_number in range(G.number_of_edges()):
            #getting the edge data of (node x, node y) in the form of a dictionary
            edge_data = G.get_edge_data(emitters[edge_number], receivers[edge_number])[0]
            #getting the info on whether the interaction was positive or negative (+1/-1)
            edge_label = edge_data['POST_LABEL']
            emitter_score[emitters[edge_number]] += edge_label
    return(emitter_score)


def positive_negative_scores_emitters(G):
    '''
    Returns the total number of positive interactions emitted by each communitiy (node)
    and the total number of negative interactions emitted by each community in the form of two dictionaries.
    '''
    emitters = np.array(G.edges)[:,0] #list of communities posting about another
    receivers = np.array(G.edges)[:,1] #list of communities being judged
    positive_score = dict.fromkeys(G.nodes(), 0)
    negative_score = dict.fromkeys(G.nodes(), 0)
    for edge_number in range(G.number_of_edges()):
        #getting the edge data of (node x, node y) in the form of a dictionary
        edge_data = G.get_edge_data(emitters[edge_number], receivers[edge_number])[0]
        #getting the info on whether the interaction was positive or negative (+1/-1)
        edge_label = edge_data['POST_LABEL']
        if edge_label == 1:
            positive_score[emitters[edge_number]] += 1
        elif edge_label == -1:
            negative_score[emitters[edge_number]] += 1
        else:
            print('Edge label not equal to -1 or 1. Edge label for edge number ', edge_number, ' is ', edge_label)
    return(positive_score, negative_score)


def edges_multiplicity(G):
    """
    Returns the multiplicity of the edges of a graph G
    """
    dic={}
    for i in G.edges():
        if i in dic:
            dic[i]+=1
        else:
            dic[i]=1
    return(dic)

def Key_Max(dic,print_values=True):
    """
    Returns the key of maximal value in the dictionnary
    """
    m=max(dic,key=dic.get)
    if print_values:
        print(m,dic[m])
    return(m)

def Key_Min(dic,print_values=True):
    """
    Returns the key of minimal value in the dictionnary
    """
    m=min(dic,key=dic.get)
    if print_values:
        print(m,dic[m])
    return(m)

def timestamp_to_seconds(timestamp):
    """
    format of timestamp: 'yyyy-mm-dd hh-mm-ss'
    returns a standard float corresponding to the number of seconds between
    your timestamp and '2013-12-31 15:39:58', which is the first timestamp of
    our graph. For the record, the 0 reference of timestamp is "1970-01-01 01:00:00"
    """
    m=match("[0-9]{4,4}[-][01][0-9][-][0-3][0-9][ ][0-2][0-9][:][0-5][0-9][:][0-5][0-9]",timestamp)
    b=bool(m) and len(timestamp)==19
    if not(b):
        raise Exception("Timestamp format should be 'yyyy-mm-dd hh-mm-ss' only.")
    my_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return(my_date.timestamp())

def seconds_to_timestamp(seconds):
    """
    takes a standard float corresponding to the number of seconds between
    your timestamp and '2013-12-31 15:39:58', which is the first timestamp of
    our graph. For the record, the 0 reference of timestamp is "1970-01-01 01:00:00"
    Returns timestamp, formated as: 'yyyy-mm-dd hh-mm-ss'
    """
    timestamp = datetime.datetime.utcfromtimestamp(seconds+1388504398.0)
    return(str(timestamp))


def All_Times(G):
    """
    Returns
    """
    l=[]
    for e in G.edges.data("TIMESTAMP"):
        l.append(timestamp_to_seconds(e[-1])-1388504398.0)
    return(sorted(l))

def Time_Growth(G):
    list_times=All_Times(G)
    list_numbers=list(range(len(list_times)))
    return(list_times,list_numbers)

def Plot_Time_Growth(list_times,list_numbers,time_div=5,fit=True):
    fig=plt.figure()
    t0=list_times[0]
    tf=list_times[-1]
    nf=list_numbers[-1]
    list_times=np.array(list_times)/tf
    list_numbers=np.array(list_numbers)/nf
    plt.plot(list_times,list_numbers,label='Network growth',color="red",alpha=1,linewidth=4, linestyle=':')
    plt.plot([list_times[0],list_times[-1]],[list_numbers[0],list_numbers[3000]*list_times[-1]/(list_times[3000]-list_times[0])],label='Linear approximation',color="orange",alpha=.5)
    plt.plot(list_times,(np.exp(list_times)-1)/(np.exp(1)-1),label='exponential approximation',color="green",alpha=1)
    if fit:
        #a,b=np.polyfit(np.exp(np.array(list_times)) , list_numbers, 1 )
        #plt.plot(list_times,a*np.exp(list_times)+b,label="exponential fit",color="orange",alpha=1)
        from scipy.optimize import curve_fit
        def func_powerlaw(x, m, c, c0):
            return c0 + x**m * c
        target_func = func_powerlaw
        popt, pcov = curve_fit(target_func, list_times, list_numbers)
        plt.plot(list_times,target_func(list_times,*popt), label=r"Powerlaw fit, $\alpha=${:.2f}".format(popt[0]), color="blue", alpha=1)
    t_ticks=[i/time_div for i in range(time_div+1)]
    y_ticks=[i/time_div for i in range(time_div+1)]
    plt.xlabel('Date')
    plt.ylabel('Total number of edges')
    plt.xticks(t_ticks,[seconds_to_timestamp(i*tf)[:10] for i in t_ticks],rotation='vertical')
    plt.yticks(y_ticks,[i*nf for i in y_ticks])    
    plt.grid('both')
    plt.legend()
    plt.tight_layout()
    return(fig)


def Largest_Connected_Component(G):
    """
    Returns a graph containing the largest connected component of the input graph
    """
    GG=G.subgraph(max(nx.connected components(G), key=len)).copy()
    return(GG)

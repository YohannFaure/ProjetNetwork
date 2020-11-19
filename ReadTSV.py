#!/usr/bin/env python3
"""
This document is supposed to be used to read the TSV file from
    http://snap.stanford.edu/data/soc-RedditHyperlinks.html
It can easilly be adapted to any tsv file.
"""


import networkx as nx

def remove_header(location):
    """
    Takes a string for the location of a text file, and removes the first line
    of the file (typically the header). The converted "example.abc" will be named "example_headless.abc".
    """
    n=location.find('.')
    f=open(location)
    lines=f.readlines()
    f2=open(location[:n]+'_headless'+location[n:],"w")
    f2.writelines(lines[1:])
    f.close()
    f2.close()
    return(None)

def remove_data(location):
    """
    Designed specificaly to deal with
    http://snap.stanford.edu/data/soc-RedditHyperlinks.html
    Returns the POST_PROPERTIES in an array and removes it from the file
    """
    f=open(location)
    lines=f.readlines()
    #l=[]
    for i in range(len(lines)):
        ni=len(lines[i]) - lines[i][::-1].find('\t') - 1
        #l.append(lines[i][ni:])
        lines[i]=lines[i][ni:]
    n=location.find('.')
    f2=open(location[:n]+'_dataless'+location[n:],"w")
    f2.writelines(lines)
    f.close()
    f2.close()
    return(None)

def get_data(location):
    """
    To get the data
    http://snap.stanford.edu/data/soc-RedditHyperlinks.html
    """
    f=open(location)
    lines=f.readlines()
    l=[]
    for i in range(len(lines)):
        ni=len(lines[i]) - lines[i][::-1].find('\t')
        l.append(lines[i][ni:])
    f.close()
    return(l)


def data_to_graph(location):
    """
    Convert the file from http://snap.stanford.edu/data/soc-RedditHyperlinks.html into a graph.
    """
    def dic_create(edge_splited):
        dic = {"POST_ID": edge_splited[2][:6], "TIMESTAMP": edge_splited[3],
               'POST_LABEL':edge_splited[4], 'POST_PROPERTIES':edge_splited[5]}
        return(dic)
    f=open(location)
    lines=f.readlines()
    header=lines[0]
    edges=lines[1:]
    G = nx.MultiGraph()
    for e in edges:
        e_splited=e.split('\t')
        dic_e=dic_create(e_splited)
        G.add_edge(e_splited[0],e_splited[1],POST_ID=dic_e['POST_ID'],
            TIMESTAMP=dic_e['TIMESTAMP'],
            POST_LABEL=dic_e['POST_LABEL'],
            POST_PROPERTIES=dic_e['POST_PROPERTIES'])
    return(G)

def data_to_digraph(location):
    """
    Convert the file from http://snap.stanford.edu/data/soc-RedditHyperlinks.html into a graph.
    """
    def dic_create(edge_splited):
        dic = {"POST_ID": edge_splited[2][:6], "TIMESTAMP": edge_splited[3],
               'POST_LABEL':int(edge_splited[4]), 'POST_PROPERTIES':edge_splited[5][:-2]}
        return(dic)
    f=open(location)
    lines=f.readlines()
    header=lines[0]
    edges=lines[1:]
    G = nx.MultiDiGraph()
    for e in edges:
        e_splited=e.split('\t')
        dic_e=dic_create(e_splited)
        G.add_edge(e_splited[0],e_splited[1],POST_ID=dic_e['POST_ID'],
            TIMESTAMP=dic_e['TIMESTAMP'],
            POST_LABEL=dic_e['POST_LABEL'],
            POST_PROPERTIES=dic_e['POST_PROPERTIES'])
    return(G)

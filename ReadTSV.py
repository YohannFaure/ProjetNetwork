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
    f=open(location)
    lines=f.readlines()
    l=[]
    for i in range(len(lines)):
        ni=len(lines[i]) - lines[i][::-1].find('\t')
        l.append(lines[i][ni:])
    f.close()
    return(l)


def data_to_graph(location):
    def dic_create(edge_splited):
        dic = {"POST_ID": edge_splited[2], "TIMESTAMP": edge_splited[3],
               'POST_LABEL':edge_splited[4], 'POST_PROPERTIES':edge_splited[5]}
        return(dic)
    f=open(location)
    lines=f.readlines()
    header=lines[0]
    edges=lines[1:]
    G = nx.Graph()
    for e in edges:
        e_splited=e.split('\t')
        dic_e=dic_create(e_splited)
        G.add_edge(e_splited[0],e_splited[1],attr=dic_e)
    return(G)

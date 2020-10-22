# ProjetNetwork

The goal here is to make some data analysis on graphs. The graph we will focus on can be found [here](https://networks.skewed.de/net/power#None_draw).

```
D.J. Watts and S.H. Strogatz, "Collective dynamics of 'small-world' networks." Nature 393, 440-442 (1998)., http://www.nature.com/nature/journal/v393/n6684/abs/393440a0.html
```

Our **main goal** is to design an attack on the power grid in order to cut power to as many nodes as possible with as little efforts as possible.

The idea behind such an attack preparation is to show the discrepancies of the system, and to create a protection or redundancy plan.

## File conversion

We will first work on the data conversion, _i.e._ converting the original file type (_.gml_) into some NetworkX understandable data.

Lucky us, it is a simple enough task, networkx has a built-in function to do that.

```
G=nx.read_gml("power.gml",label='id')
```

> **Note:** We decided to create a tool to read `.tsv` files, as our first network choice was different. This could be useful if we ever need to read a `.tsv` graph at some point. The module associated with that is named `ReadTSV.py`. The graph associated can be found [here](http://snap.stanford.edu/data/soc-RedditHyperlinks.html)

## Information gathering

We need to find information about the graph.

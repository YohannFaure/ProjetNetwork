# ProjetNetwork

The goal here is to make some data analysis on graphs. The graph we will focus on can be found [here](https://networks.skewed.de/net/power#None_draw).

```
D.J. Watts and S.H. Strogatz, "Collective dynamics of 'small-world' networks." Nature 393, 440-442 (1998)., http://www.nature.com/nature/journal/v393/n6684/abs/393440a0.html
```

## File conversion

We will first work on the data conversion, _i.e._ converting the original file type (_.gml_) into some NetworkX understandable data.

Lucky us, it is a simple enough task, networkx has a built-in function to do that.

```
G=nx.read_gml("power.gml",label='id')
```

> **Note:** This was too simple, so we decided to create a tool to read `.tsv` files. This could be useful if we ever need to read a `.tsv` graph at some point. The module associated with that is named `ReadTSV.py`.

# ProjetNetwork
*Flora Gaudillère*  
*Yohann Faure*



This project aims at studying an interaction graph in the social network [reddit](https://www.reddit.com/). The data used can be found [here](http://snap.stanford.edu/data/soc-RedditHyperlinks.html).[^1]

[^1]: S. Kumar, W.L. Hamilton, J. Leskovec, D. Jurafsky. Community Interaction and Conflict on the Web. World Wide Web Conference, 2018.


Our **main goal** is to get familiar with the data structure**s** offered by `Networkx`, and to implement simple algorithms over said structures.


[TOC]



---

## Understanding the data

### How reddit works

In a nutshell, Reddit allows users to create communities, dedicated to a specific topic, named *subreddits*, designed by r/their name. For example the subreddit `r/cats` talks about cats. In a given community, one can then post images, text, or links, and redditors (the users of reddit) can then either upvote (like) ou downvote (dislike) the post.

### What's in the data

The network represents the directed connections between two subreddits, a connection being a post containing a direct hyperlink to an other subreddit. The network is extracted from publicly available Reddit data of 2.5 years from Jan 2014 to April 2017.

Each hyperlink is annotated with a value named `POST_LABEL`, which can either be $-1$ or $+1$, and that reflects the sentiment of the source post towards the target post. $-1$ means the source community is negatively judging the target, while $+1$ means the source is positively judging the target.

The way such label has been put onto every post is detailed in [this study](http://snap.stanford.edu/conflict/), but basically, it is done using Deep Learning.

The network is, by essence, directed, temporal, and attributed.


## File conversion : `ReadTSV.py`

First, we have to work on the data conversion, *i.e.* converting the original data, stored in a `.tsv` file into some NetworkX understandable format.

To do so, we created a python module composed of a few key functions, made specifically for this `.tsv` file format, and specialized for our data.

### Introducing MultiGraphs

The first attempt at reading the data let to edges being multiple times written, because 



## Information gathering

We need to find information about the graph.


```abc
X:1
T:La Patrouille des Éléphants
M:4/4
C:Disney
K:F
A1/2^G1/2 |: AF FF F3/2 A1/2^G1/2 | AF EF G3/2 B1/2A1/2| B GG B1/2A1/2 B GGz|
c2c2c2z c1/2c1/2 | cB AG c3/2 c1/2c1/2 | cB AG F3/2 A1/2^G1/2 :|
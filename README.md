# ProjetNetwork
*Flora Gaudillère*  
*Yohann Faure*



This project aims at studying an interaction graph in the social network [reddit](https://www.reddit.com/)<sup id="a1">[1](#f1)</sup>. The data used can be found [here](http://snap.stanford.edu/data/soc-RedditHyperlinks.html).<sup id="a2">[2](#f2)</sup>



Our **main goal** is to get familiar with the data structure**s** offered by `Networkx`, and to implement simple algorithms over said structures.


[TOC]



---

## 1 - Understanding the data

### 1.1 - How reddit works

In a nutshell, Reddit allows users to create communities, dedicated to a specific topic, named *subreddits*, designed by `r/their name`. For example the subreddit `r/cats` talks about cats. In a given community, one can then post images, text, or links, and redditors (the users of reddit) can then either upvote (like) ou downvote (dislike) the post.

### 1.2 - What is in the data

The network represents the directed connections between two subreddits, a connection being a post containing a direct hyperlink to an other subreddit. The network is extracted from publicly available Reddit data of 2.5 years from Jan 2014 to April 2017.

<a name="POST_LABEL"></a>

Each hyperlink is annotated with a value named `POST_LABEL`, which can either be $-1$ or $+1$, and that reflects the sentiment of the source post towards the target post. $-1$ means the source community is negatively judging the target, while $+1$ means the source is positively judging the target.

The way such label has been put onto every post is detailed in [this study](http://snap.stanford.edu/conflict/), but basically, it is done using Deep Learning.

The network is, by essence, directed, temporal, and attributed.

> **Note:** the date in the data is wrong. For example the datestamp of `POST_ID=34c15a`, from `r/changelog` to `r/redditdev`, is `2015-04-27`, while the real datestamp of this post is `2015-04-30`.

### 1.3 - Dynamics : Interactions or relations?

This data is a collection of ponctual interactions between subreddits, but studying the frequency and the value of said interactions can lead to the construction of relations, the same a a relationship between two individuals is a succession of interactions.

We don't take into account the creation date of a subreddit, but such information is made available on the reference paper.

## 2 - File conversion : `ReadTSV.py`

First, we have to work on the data conversion, *i.e.* converting the original data, stored in a `.tsv` file into some NetworkX understandable format.

To do so, we created a python module composed of a few key functions, made specifically for this `.tsv` file format, and specialized for our data.

### 2.1 - Introducing MultiGraphs

The first attempt at reading the data led to edges being multiple times written, because most communities refers to themselves mutiple times. For example `r/trendingsubreddits` reffered to `r/changelog` 548 times, while the other way around, there is no post refering `r/trendingsubreddits` in `r/changelog`.

What is happening here is that there is a [post](https://www.reddit.com/r/changelog/comments/22pz96/reddit_change_trending_subreddits_on_the_front/) in `r/changelog`, created 2 days before the begining of the data collection, that mentioned a new functionality added to Reddit : a new subreddit (`r/trendingsubreddits`) in which is automatically posted every day the list of the best-performing subreddits of the day. Then, each post of this subreddit contained a link to this `r/changelog` post.

> What's this? We've started displaying a small selection of [trending subreddits on the front page](https://www.reddit.com/r/changelog/comments/22pz96/reddit_change_trending_subreddits_on_the_front/). Trending subreddits are determined based on a variety of activity indicators (which are also limited to safe for work communities for now). Subreddits can choose to opt-out from consideration in their subreddit settings.  
><div style="text-align: right"><cite>Every post in r/trendingsubreddits</cite></div>

### 2.2 - Selectionning information

In order to have a cleaner understanding of the data, and to represent this understanding, we decided to pre-select the data before introducing it into the networkx graph. We decided to create separate keys for the `POST_ID` (which is unique accros all posts, and therefore useful tu distinguish them), `TIMESTAMP` (in case we want to study a time-dependant property), and `POST_LABEL` (the positive or negative [review of the post](#POST_LABEL)).

All the rest f the data is stored raw from the `.tsv` file in `POST_PROPERTIES`, just in case we need it, but we did not use it in this project.

### 2.3 - Converting the file

```
>>> import networkx as nx
>>> import ReadTSV
>>> G=ReadTSV.data_to_digraph('body.tsv')
>>> G
<networkx.classes.multidigraph.MultiDiGraph object at 0x7f4d6c653850>
```

## 3 - Getting in touch with the data structure

### 3.1 - Storing the analysis functions : `Network_Analysis.py`

We  decided to group all of our functions in a single python file called `Network_Analysis.py`. This way, a simple `import Network_Analysis as NA`
allows us to use them seamlessly in the scripts.

To get details on the content of this module, feel free to use the following commands:
```
>>> import Network_Analysis as NA
>>> help(NA)
```

### 3.2 - First informations

In order to really understand the data structure of the graph, we fist wanted to plot it. But we had to check a few things before doing so.

```
>>> len(G.nodes)
35776
>>> len(G.edges)
286561
```

Plotting it might therefore not be an excellent idea. The graph is indeed too large to get a proper display using Networkx standard `draw` method. We could imagine a drawing method based on a cut of the graph, for example we could select the higest degree nodes and only plot them.

### 2.3 - Degree cutting

To cut according to the degree of the nodes, we need to find out what the distribution of the degrees is. To do so, we designed two functions called `degree_distribution`, and `Degree_distribution_plot`, that do just what their name indicate.

```
NA.Degree_distribution_plot(G)
```
![Degree_distribution_plot](./figures/Degree_distribution_plot.png)

This plot is quitte interesting, as it tells us that the distribution of degrees is broad, and might be called "scale-free". Here though, this is not a caracteristic of interest, therefore we will avoid all controversy and not call it "scale-free", just "with a broad degree distribution".

### 3.4 - Ploting

Now that we know that the distribution is broad, we can simply cut it on the degree, as such a cut would still preserve the overall structure of the graph, at least for visual inspection.

That is what `NA.degree_cut` does. It cuts the graph to only keep the highest degree nodes. One can specify the "degrees" on which to cut, making it more of a generic cut function. For example `degree_cut(G,2000,degrees=dic)` would return a graph composed of only the nodes of `G` with a score given by the dictionnary `dic` higher than 2000.

Let's plot it, using `NA.GraphDraw`. This function has a second argument that allows the selection of the interaction to plot (positive, negative, or total).

```
>>> GG=NA.degree_cut(G,2500)
>>> NA.GraphDraw(GG,1)
>>> NA.GraphDraw(GG,-1)
```

![GraphDraw1](./figures/GraphDraw1.png)
![GraphDraw2](./figures/GraphDraw2.png)

### 3.5 - Converting to non-multi Graph

One of the first ideas we had too was to create conversion tools to make a simple Graph out of the MultiGraph. To do so, one simply needs to use `NA.MultigraphToGraph`. It allows us to better manipulate the graph.

> We also made a function to convert a Directed Graph into a simple Graph, but such manipulation looses the very essence of this dataset.

## Data Analysis

It is now time to answer a few questions, such as "which community recieves the most hated of all reddit?", "which community is most appreciated?", or "what community clusters can be found?".

### Simple reception metrics

```
>>> positive_score, negative_score=NA.positive_negative_scores(GG)
>>> total_score={i:positive_score[i]-negative_score[i] for i in positive_score}
>>> most_loved = NA.Key_Max(positive_score)
askreddit 6525
>>> most_hated = NA.Key_Max(negative_score)
askreddit 804
>>> best_scoring = NA.Key_Max(total_score)
askreddit 5721
```

The most hated, most loved, and best scoring subreddit is, without surprise, `r/askreddit`, a subreddit dedicated to asking questions about almost anything to the Reddit community.

But this is not very interesting, we might want to find the second and third subreddits. After a few tribulations, the results are the following:

<div style="text-align: right">

| Love score | Hate score | Worst total score |
| -------- | -------- | -------- |
| r/askreddit 6525 | r/askreddit 804 |r/latterdaysaints -52 |
|r/iama 3462 |r/news 484 |r/ketorecipes -31 |
|r/pics 2533 |r/todayilearned 414 |r/femradebates -25 |
|r/writingprompts 2454 |r/worldnews 407 |r/lifeafternarcissism -19 |
|r/leagueoflegends 2251 |r/kotakuinaction 388 |r/nsfw_gifs -14 |
|r/videos 2235 |r/pics 246 |r/fitnesscirclejerk -13 |
|r/todayilearned 1957 |r/iama 232 |r/civcraftexchange -13 |
|r/worldnews 1850 |r/showerthoughts 221 |r/triviatime -11 |
|r/funny 1847 |r/videos 211 |r/idg0d -10 |
|r/nfl 1381 |r/adviceanimals 208 |r/thebatmanteam -9 |

</div>


### Simple emission metrics

Who are the biggest haters ?

to do

### General time growth of Reddit

Done, to writte

### Louvain

to do

---

<sup id="f1">1</sup> Let's be honnest, this whole Master is just an excuse to spend hours on social networks every day. [↩](#a1)

<sup id="f2">2</sup> S. Kumar, W.L. Hamilton, J. Leskovec, D. Jurafsky. Community Interaction and Conflict on the Web. World Wide Web Conference, 2018. [↩](#a2)



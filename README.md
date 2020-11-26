# ProjetNetwork
*Yohann Faure*  
*Flora Gaudillière*




This project aims at studying an interaction graph in the social network [reddit](https://www.reddit.com/)<sup id="a1">[1](#f1)</sup>. The data used can be found [here](http://snap.stanford.edu/data/soc-RedditHyperlinks.html).<sup id="a2">[2](#f2)</sup>



Our **main goal** is to get familiar with the data structure**s** offered by `Networkx`, and to implement simple algorithms over said structures.


[TOC]



---

## 1 - Understanding the data

### 1.1 - How reddit works

In a nutshell, Reddit allows users to create communities dedicated to a specific topic, named *subreddits*, designed by `r/their_name`. For example the subreddit `r/cats` talks about cats. In a given subreddit, one can then post images, text, or links, and redditors (the users of reddit) can then either upvote (like) ou downvote (dislike) the post.

### 1.2 - What is in the data

The network represents the directed connections between two subreddits, a connection being a post containing a direct hyperlink to another subreddit in the text body (as opposed to the title of the post). The network is extracted from publicly available Reddit data of 2 years and a half, from January 2014 ($t_0$) to April 2017 ($t_f$).

<a name="POST_LABEL"></a>

Each hyperlink is annotated with a value named `POST_LABEL`, which can either be $-1$ or $+1$, and that reflects the sentiment of the source post towards the target post. $-1$ means the source subreddit is negatively judging the target, while $+1$ means the source is positively judging the target.

The way the labels have been determined is detailed in [this study](http://snap.stanford.edu/conflict/), but basically, it is done using Deep Learning.

The network is, by essence, directed, temporal, and attributed.

> **Note:** the date in the data is wrong. For example the datestamp of `POST_ID=34c15a`, from `r/changelog` to `r/redditdev`, is `2015-04-27`, while the real datestamp of this post is `2015-04-30`.

### 1.3 - Dynamics: Interactions or relations?

This data is a collection of ponctual interactions between subreddits, but studying the frequency and the value of said interactions can lead to the construction of relations, in the way same as a relationship between two individuals is a succession of interactions.

We don't take into account the creation date of a subreddit, but such information is made available in the reference paper.

## 2 - File conversion: `ReadTSV.py`

First, we have to work on the data conversion, *i.e.* converting the original data, stored in a `.tsv` file, into some NetworkX understandable format.

To do so, we created a python module composed of a few key functions, made specifically for this `.tsv` file format, and specialized for our data.

### 2.1 - Introducing MultiGraphs

The first attempt at reading the data led to edges being written multiple times, because a lot of subreddits refer to another given subreddit mutiple times. For example `r/trendingsubreddits` refered to `r/changelog` 548 times, while the other way around, there is no post refering `r/trendingsubreddits` in `r/changelog`.

What is happening here is that there is a [post](https://www.reddit.com/r/changelog/comments/22pz96/reddit_change_trending_subreddits_on_the_front/) in `r/changelog`, created 2 days before the begining of the data collection, that mentioned a new functionality added to Reddit : a new subreddit (`r/trendingsubreddits`) in which is automatically posted every day the list of the best-performing subreddits of the day. Then, each post of this subreddit contained a link to this `r/changelog` post.

> What's this? We've started displaying a small selection of [trending subreddits on the front page](https://www.reddit.com/r/changelog/comments/22pz96/reddit_change_trending_subreddits_on_the_front/). Trending subreddits are determined based on a variety of activity indicators (which are also limited to safe for work subreddits for now). Subreddits can choose to opt-out from consideration in their subreddit settings.  
><div style="text-align: right"><cite>Every post in r/trendingsubreddits</cite></div>

### 2.2 - Selecting information

In order to have a better understanding of the data, and to represent this understanding, we decided to pre-select the data before introducing it into the networkx graph. We decided to create separate keys for the `POST_ID` (which is unique accros all posts, and therefore useful tu distinguish them), `TIMESTAMP` (in case we want to study a time-dependent property), and `POST_LABEL` (the positive or negative [review of the post](#POST_LABEL)).

The rest of the data is stored raw from the `.tsv` file in `POST_PROPERTIES`, just in case we need it, but we did not use it in this project.

### 2.3 - Converting the file

```python
>>> import networkx as nx
>>> import ReadTSV
>>> G=ReadTSV.data_to_digraph('body.tsv')
>>> G
<networkx.classes.multidigraph.MultiDiGraph object at 0x7f4d6c653850>
```

## 3 - Getting in touch with the data structure

### 3.1 - Storing the analysis functions: `Network_Analysis.py`

We  decided to group all of our functions in a single python file called `Network_Analysis.py`. This way, a simple `import Network_Analysis as NA`
allows us to use them seamlessly in the scripts.

To get details on the content of this module, feel free to use the following commands:
```python
>>> import Network_Analysis as NA
>>> help(NA)
```

### 3.2 - First approach

In order to really understand the data structure of the graph, we fist wanted to plot it. But we had to check a few things before doing so.

```python
>>> len(G.nodes)
35776
>>> len(G.edges)
286561
```

Plotting it might therefore not be an excellent idea. The graph is indeed too large to get a proper display using Networkx's standard `draw` method. We could imagine a drawing method based on a cut of the graph, for example we could select the higest degree nodes and only plot these.

### 3.3 - Degree cutting

To cut according to the degree of the nodes, we need to find out what the distribution of the degrees is. To do so, we designed two functions called `degree_distribution`, and `Degree_distribution_plot`, that do just what their names indicate.

```python
>>> NA.Degree_distribution_plot(G)
```

![Degree_distribution_plot](https://i.imgur.com/7hfJUBq.png)


This plot is quitte interesting, as it tells us that the distribution of degrees is broad, and might be called "scale-free". Here though, this is not a caracteristic of interest, therefore we will avoid all controversy and not call it "scale-free", just "with a broad degree distribution".

### 3.4 - Plotting

Now that we know that the distribution is broad, we can simply cut it on the degree, as such a cut would still preserve the overall structure of the graph, at least for visual inspection.

That is what `NA.degree_cut` does. It cuts the graph to only keep the highest degree nodes. 

> NB: One can specify the "degrees" on which to cut, making it more of a generic cut function. For example `degree_cut(G,2000,degrees=dic)` would return a graph composed of only the nodes of `G` with a score given by the dictionnary `dic` higher than 2000.

Let's plot it, using `NA.GraphDraw`. This function has a second argument that allows the selection of the interactions to plot (positive, negative, or total).

```python
>>> GG=NA.degree_cut(G,2500)
>>> NA.GraphDraw(GG,1)
>>> NA.GraphDraw(GG,-1)
```

![GraphDraw1](https://i.imgur.com/C3HckCv.png)

![GraphDraw2](https://i.imgur.com/jW9PB1L.png)


### 3.5 - Converting to non-multi Graph

Another idea we had was to create conversion tools to make a simple Graph out of the MultiGraph. To do so, one simply needs to use `NA.MultigraphToGraph`. It allows us to better manipulate the graph.

> We also made a function to convert a Directed Graph into a simple Graph, but such manipulation looses the very essence of this dataset.

## 4 - Data Analysis

It is now time to answer a few questions, such as "which subreddit receives the most hate in all of reddit?", "which subreddit is the most appreciated?", or "what subreddit clusters can be found?".

### 4.1 - Simple reception metrics

We designed a set of function to find out the most loved and hated subreddits. Their usage goes as follows :

```python
>>> positive_score, negative_score=NA.positive_negative_scores(G)
>>> total_score={i:positive_score[i]-negative_score[i] for i in positive_score}
>>> most_loved = NA.Key_Max(positive_score)
askreddit 6525
>>> most_hated = NA.Key_Max(negative_score)
askreddit 804
>>> best_scoring = NA.Key_Max(total_score)
askreddit 5721
```

The most hated, most loved, and best scoring subreddit is, without surprise, `r/askreddit`, a subreddit dedicated to asking questions about almost anything to Reddit users.

But this is not very interesting. We might want to find the second and third subreddits. After a few tribulations, the results are the following:

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


### 4.2 - Simple emission metrics

Conversely, we might ask ourselves what are the subreddits that judge others most positively or negatively.

```python
>>> positive_score, negative_score=NA.positive_negative_scores(G)
>>> total_score={i:positive_score[i]-negative_score[i] for i in positive_score}
>>> most_loved = NA.Key_Max(positive_score)
subredditdrama 3035
>>> most_hated = NA.Key_Max(negative_score)
subredditdrama 1630
>>> best_scoring = NA.Key_Max(total_score)
outoftheloop 1836
```


Unsurprisingly, the subreddit with both the highest positive and negative judgement scores is `r/subredditdrama`, a subreddit dedicated to judging other subreddits (we might add, on a positive note, that the positive judgements outweight the negatives ones by a very large margin). 

Subreddits such as `r/drama`, `r/bestofoutrageculture` or `r/badhistory` are also a groups that we could expect to find in the subreddits with the highest negative judgement scores.

<div style="text-align: right">

| Lover score | Hater score | Worst total score |
| -------- | -------- | -------- |
| r/subredditdrama 3035 | r/subredditdrama 1630 |r/shitghazisays -65 |
| r/outoftheloop 1897 | r/drama 497 | r/femrameta -56 |
| r/circlebroke 1873 |r/circlebroke 485 |  r/mubookclub -45 |
| r/shitliberalssay 1605 | r/copypasta 464 | r/hhcjcopypasta -30 |
| r/hailcorporate 1479 | r/circlejerkcopypasta 375 | r/nolibswatch -30 |
| r/writingprompts 145 | r/shitliberalssay 363 | r/iosthemes -28 |
| r/copypasta 1360 |  r/bestofoutrageculture 309 | r/wherearethefeminists -24 |
| r/buildapc 1303 | r/conspiracy 293 |  r/warcraftlore -18 |
| r/tipofmypenis 1185 | r/writingprompts 251 |  r/wowcirclejerk -15 |
| r/conspiracy 1169 | r/badhistory 219 | r/metaphotography -15 |

</div>

> Some results are a bit surprising: for example, `r/hailcorporate` appears to be a loving subreddit. Yet the description of the subreddit is
> > /r/HailCorporate is to document times when people act as unwitting advertisers for a product as well as to document what appear to be legitimate adverts via [native advertising](https://en.wikipedia.org/wiki/Native_advertising).
>
> After an inspection of it's content, it clearly is a denunciation subreddit, and therefore should have a high Hater Score. For example the post with id [4isap0](http://www.reddit.com/r/HailCorporate/comments/4isap0/only_24_hrs_after_the_reddit_logo_is_replaced_by/) is clearly a negative one. It calls out the use of native advertising to artificially boost the rating of the first Deadpool movie. Yet, it has a positive `POST_LABEL`, which means it is supposed to be a positive review.
> 
> More details on that issue [later](#5---Critical-analysis-of-the-data).


### 4.3 - General time growth of Reddit

One of the interesting things about networks is their growth. We can use this data to evaluate how fast Reddit has grown in this time scale. The basic hypothesis we made here is that the number of posts in an amount of time is proportional to the number of active members of the social network.

On the following graph, we represented in dashed lines the actual number of posts in fonction of time. The yellow line corresponds to the expected shape of such a number if the number of users was constant. It is obtained by simply approximating the curve by its tangeant at $t=t_0$. The green line is an exponential approximation of the curve, with initial and final numbers of posts fixed. Finaly the blue cruve is a powerlaw fit.

![Plot_Time_Growth](https://i.imgur.com/l9Xvbhj.png)


The result here is that the powerlaw fit is clearly a better one than the exponential fit. It is interesting in itself to make predictions on the growth of Reddit, in order to prepare its infrastucture for the future, for example, but it might be interesting to compare that to the number of nodes, *i.e.* the number of subreddits.

If we had the creation date of all subreddits, we could compare $N(t)$ the number of subreddits to $E(t)$ the number of posts referencing them, and compute a *Densification exponent*<sup id="a3">[3](#f3)</sup> $\alpha$ (if any). Such exponent exists if there is a law:

$$
E(t)\propto N(t)^\alpha
$$

In that case, usually, $1<\alpha<2$, 1 corresponding to a tree (the minimum for the network to be convex, and therefore studied as one single network instead of two separate networks), and 2 corresponding to a clique. In our case, such exponent could be over 2 as the graph is a MultiGraph, each node can be (and usually is) connected twice or more to the same other node.



## 5 - Communities of subreddits

### 5.1 - Position of the problem

An interesting aspect of this dataset is that it links subreddits, and can therefore describe communities, *i.e.* ensembles of subreddits that respond to one another and communicate. The goal of this section is to use the [Louvain Algorithm](https://en.wikipedia.org/wiki/Louvain_method) to detect such communities.

The first problem here is that the Louvain algorithm only takes the type `Graph` as input. We could have used a community structure detection algorithm with directed graphs, but we wanted to keep things simple. We therefore had to make a data conversion.

The second problem is the the number of nodes: there are many nodes disconnected from the main connected component. Therefore, to avoid detecting useless communities of 1, 2 or 3 subreddits, we decided to only keep the nodes of highest degree. This comes with a major drawback: cutting nodes reduces the community structure of Reddit. This cut has to be at a low degree, and we decided 200 to be the cutoff. 

```python
# Cutting on degree
GG=NA.degree_cut(G,200)
# Defining a weight for the edges
_,l1,l2=NA.edge_evaluation(GG)
weight={i:l1[i] for i in l1}
# Making the MultiDiGraph a Graph
GGG=NA.DiGraphToGraph(NA.MultigraphToGraph(GG,l1))
```

### 5.2 - Creating the algorithm

The Louvain algorithm in itself stems from a module designed specifically for it:
```bash
pip3 install -U git+https://github.com/taynaud/python-louvain.git@networkx2
```

We created a Python module named `Community_Detection`, containing all the necessary functions. Once a proper graph is created, the communities can be both generated and plotted using 


```python
import Community_Detection as CD
partition = CD.plot_community(GGG)
```


![](https://i.imgur.com/GPLfYz5.png)


The community structure created above is made using the positive edges only, but other weights would be conceivable.

Here the size of the circles are proportional to the degree of each node, while their position is computed using a spring layout inside the community. The details are rather boring and did not make it to the final report, feel free to read the code.

> Some highlights on the difficulties we encountered here:  
> We had to decide colors and size for the communities and their text, and we wanted it ro be proportional to their degree. That was quite painful as Networkx only has a partial support for such functionnalities.  
> An other difficulty is the resolution of the image. It has to be adjusted for every network, and that can take a while.


### 5.3 - Analysis of the communities

The main observation here is that we end up with 6 macro-communities with very distinct main topics, which are listed in the table below.


| Sports (with a visible American Football sub-community on the left)| Technology (with cryptocurrencies in the top-right corner) | Free speeking (helping communities, sexuality, safe spaces) |
|---|---|---|
| ![](https://i.imgur.com/4I6mJPd.png) | ![](https://i.imgur.com/Oj9ob9J.png) | ![](https://i.imgur.com/OeAMrzo.png) |

| Video games and geek culture (note: it contains SubRedditDrama) | Politics, Religion and News (and also conspiracies) | Humor? (this community is hard to define) |
|-|-|-|
| ![](https://i.imgur.com/YvE5Ptm.png) | ![](https://i.imgur.com/ZwpaWLq.png) | ![](https://i.imgur.com/YvEUVFa.png)|

It is interesting to note that some subreddits end up in categories one would not necessarily have expected them to, for example r/Soccer which ended up in the political community instead of the Sports community.

> This specific difference can be explained by the fact that all european countries' subreddits are in the political community, and that soccer is more of a European sport while the Sports subreddit is highly US-centered, with a major emphasis on American football.

### 5.4 - Limits of this community mapping

The first limit here is that some communities are really close one to an other : technology and video games are so close that `r/BuildaPCforMe` ended up in video games while being clearly closer to technology topic-wise. Likewise, some important subcommunities would deserve their own community, such as American Football.

The next major drawback is that this representation used a degree cut, and is higly dependent on that cut, as we discovered while experimenting. The higher the degree cutoff is, the worse the communities are. A simple explanation for this phenomena is that loosing small subreddits is loosing links of lenght 2 between big subreddits.

Finally this algorithm is not deterministic: it involves pseudo-random functions. Here is an other output for example, where the communities are slightly different, using the exact same function twice.

![](https://i.imgur.com/XSNlPHP.png)





## 6 - Critical analysis of the data

### 6.1 - Flawed Cases

As mentionned earlier, the dataset appears to be flawed, especially on some of the evaluations of positiveness or negativeness for posts. We mentioned the example of `r/HailCorporate` being a mostly negative subreddit yet having a mostly positive Emission score. This is not the only case we can find. `r/ShitLiberalsSay`, dedicated to the criticism of Liberal (~centrist) political views in the US, is mainly composed of users with Left Wing opinions. Yet only 6 out of its 24 references to `r/The_Donald` (a banned subreddit in support of D. Trump) are considered negative.

Similarly, in `r/HateSubsInAction`, dedicated to judging the most hateful subreddits (racism, bigotry, etc.), we can find a positive review of `r/The_Donald`. This review is obviously negative ([4mbmlx](http://www.reddit.com/r/HateSubsInAction/comments/4mbmlx/fun_soviet_reactionary_thread_on_the_donald/)), but it is considered as positive.

### 6.2 - A proposition of explanation

After diving into the depths  of Reddit, and following the most suspicious results of our study, we found out that it was almost almost impossible to find a false negative review of a subreddit, while false positive are all around the corner.

Our interpretation is that the Neural Network used to determine the positivity of a post developped a very high treshold for negative reviews, considering something negative only when very explicit caracteristics appeared. Therefore, the results of community detection using the positive scores can be highly misleading, sorting together `r/The_Donald` and `r/Democrats` for example!

The Neural Network's difficulty to label posts as negative is not surprising if you consider the fact that it is very difficult to train an algorithm to recognize social cues (for instance second degree) that are used in posts making fun of other subreddits: without an explicit statement of negative judgement, this kind of post is sorted as "positive", completely missing the actual meaning of the interaction. 



---

<sup id="f1">1</sup> Let's be honest, this whole Master is just an excuse to spend hours on social networks every day. [↩](#a1)

<sup id="f2">2</sup> S. Kumar, W.L. Hamilton, J. Leskovec, D. Jurafsky. Community Interaction and Conflict on the Web. World Wide Web Conference, 2018. [↩](#a2)

<sup id="f3">3</sup> J. Leskovec, J. Kleinberg, C. Faloutsos. Graphs over time: densification laws, shrinking diameters and possible explanations, 2005. [↩](#a3)



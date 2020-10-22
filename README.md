# ProjetNetwork

The goal here is to make some data analysis on graphs. The graph we will focus on can be found [here](http://snap.stanford.edu/data/soc-RedditHyperlinks.html).

```
@inproceedings{kumar2018community,
  title={Community interaction and conflict on the web},
  author={Kumar, Srijan and Hamilton, William L and Leskovec, Jure and Jurafsky, Dan},
  booktitle={Proceedings of the 2018 World Wide Web Conference on World Wide Web},
  pages={933--943},
  year={2018},
  organization={International World Wide Web Conferences Steering Committee}
}
```

## File conversion

We will first work on the data conversion, _i.e._ converting the original file type ($\texttt{.tsv}$) into some NetworkX understandable data.

The data file is in tab separated format :

```
SOURCE_SUBREDDIT tab TARGET_SUBREDDIT tab POST_ID tab TIMESTAMP tab POST_LABEL tab POST_PROPERTIES
```

Example (excluding the POST_PROPERTIES):

```
leagueoflegends teamredditteams 1u4nrps 2013-12-31 16:39:58     1
```

POST_PROPERTIES: a vector representing the text properties of the source post, listed as a list of comma separated numbers. The vector elements are the following:

```
1. Number of characters
2. Number of characters without counting white space
3. Fraction of alphabetical characters
4. Fraction of digits
5. Fraction of uppercase characters
6. Fraction of white spaces
7. Fraction of special characters, such as comma, exclamation mark, etc.
8. Number of words
9. Number of unique works
10. Number of long words (at least 6 characters)
11. Average word length
12. Number of unique stopwords
13. Fraction of stopwords
14. Number of sentences
15. Number of long sentences (at least 10 words)
16. Average number of characters per sentence
17. Average number of words per sentence
18. Automated readability index
19. Positive sentiment calculated by VADER
20. Negative sentiment calculated by VADER
21. Compound sentiment calculated by VADER
22. LIWC_Funct
23. LIWC_Pronoun
24. LIWC_Ppron
25. LIWC_I
26. LIWC_We
27. LIWC_You
28. LIWC_SheHe
29. LIWC_They
30. LIWC_Ipron
31. LIWC_Article
32. LIWC_Verbs
33. LIWC_AuxVb
34. LIWC_Past
35. LIWC_Present
36. LIWC_Future
37. LIWC_Adverbs
38. LIWC_Prep
39. LIWC_Conj
40. LIWC_Negate
41. LIWC_Quant
42. LIWC_Numbers
43. LIWC_Swear
44. LIWC_Social
45. LIWC_Family
46. LIWC_Friends
47. LIWC_Humans
48. LIWC_Affect
49. LIWC_Posemo
50. LIWC_Negemo
51. LIWC_Anx
52. LIWC_Anger
53. LIWC_Sad
54. LIWC_CogMech
55. LIWC_Insight
56. LIWC_Cause
57. LIWC_Discrep
58. LIWC_Tentat
59. LIWC_Certain
60. LIWC_Inhib
61. LIWC_Incl
62. LIWC_Excl
63. LIWC_Percept
64. LIWC_See
65. LIWC_Hear
66. LIWC_Feel
67. LIWC_Bio
68. LIWC_Body
69. LIWC_Health
70. LIWC_Sexual
71. LIWC_Ingest
72. LIWC_Relativ
73. LIWC_Motion
74. LIWC_Space
75. LIWC_Time
76. LIWC_Work
77. LIWC_Achiev
78. LIWC_Leisure
79. LIWC_Home
80. LIWC_Money
81. LIWC_Relig
82. LIWC_Death
83. LIWC_Assent
84. LIWC_Dissent
85. LIWC_Nonflu
86. LIWC_Filler
```

Example :

```
345.0,298.0,0.75652173913,0.0173913043478,0.0869565217391,0.150724637681,0.0753623188406,57.0,53.0,10.0,4.78947368421,15.0,0.315789473684,1.0,1.0,345.0,57.0,35.5778947368,0.073,0.08,0.1748,0.3448275862068966,0.05172413793103448,0.034482758620689655,0.0,0.034482758620689655,0.0,0.0,0.0,0.017241379310344827,0.05172413793103448,0.10344827586206896,0.05172413793103448,0.0,0.10344827586206896,0.0,0.034482758620689655,0.034482758620689655,0.06896551724137931,0.017241379310344827,0.034482758620689655,0.0,0.0,0.10344827586206896,0.0,0.0,0.0,0.05172413793103448,0.017241379310344827,0.034482758620689655,0.0,0.0,0.017241379310344827,0.1896551724137931,0.034482758620689655,0.0,0.034482758620689655,0.034482758620689655,0.0,0.0,0.06896551724137931,0.05172413793103448,0.034482758620689655,0.034482758620689655,0.0,0.0,0.017241379310344827,0.017241379310344827,0.0,0.0,0.0,0.06896551724137931,0.017241379310344827,0.05172413793103448,0.0,0.05172413793103448,0.06896551724137931,0.034482758620689655,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
theredlion      soccer  1u4qkd  2013-12-31 18:18:37     -1      101.0,98.0,0.742574257426,0.019801980198,0.049504950495,0.0594059405941,0.178217821782,14.0,14.0,2.0,5.71428571429,1.0,0.0714285714286,2.0,0.0,49.5,7.0,16.0492857143,0.472,0.0,0.5538,0.06666666666666667,0.06666666666666667,0.06666666666666667,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.13333333333333333,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.06666666666666667,0.0,0.06666666666666667,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
inlandempire    bikela  1u4qlzs 2014-01-01 14:54:35     1       85.0,85.0,0.752941176471,0.0235294117647,0.0823529411765,0.0117647058824,0.211764705882,10.0,10.0,2.0,7.2,0.0,0.0,1.0,0.0,85.0,10.0,23.605,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.09090909090909091,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.09090909090909091,0.09090909090909091,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.09090909090909091,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0

```

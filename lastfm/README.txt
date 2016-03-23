-----------------------------------
ARS Mid-Term 2016 - Data Collection
-----------------------------------

Instruction:

1) Download a sample of the Last.fm social graph (5-10k users per group) using Network.py
2) Clean the obtained graph using CleanNetwork.py

Tips:
1) Network.py require a Lastfm api key in order to be executed: register one at http://www.lastfm.it/api
2) Network.py needs a seed username to start the snowball sampling: select randomly a user from lastfm avoiding nodes having more than 50 neighbors. Each group MUST choose a different seed node.
3) Network.py can be parametrized w.r.t. the number of user and listening per user to fetch.
4) The download process will take time (hours): relax and be patient :)

Dependencies:

The scripts provided require: lastfm, and networkx libraries (the latter are included in the project folder supplied).

----------------------------------------
WMR Mid-Term 2015 - Preliminary Analysis
----------------------------------------

Once collected a network sample, each group must analyze it using one of the tools discussed in class (i.e. networkx, Cytoscape, Gephi).
The networkx library reference can be found at: http://networkx.github.io/documentation/networkx-1.9/reference/index.html

The network analysis should at least include (but not necessarily be restricted to):
- Degree Distribution
- Clustering Coefficient
- Connected Components
- Shortest paths
- Centrality Measures
- ...

The results of the analysis have to be discussed in a written survey.
The code produced and data collected are part of the project submission.

Application name	MyZanichelli
API key	2e8e6091dbf709e685740dc8987ff657
Shared secret	a1ab0b3d7353d945545acd424323b9d6
Registered to	vslovik
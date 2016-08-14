OPERA NETWORK ANALYSIS
----------------------

Social network analytics course. Final project

Data source: GBOPERA MAGAZINE www.gbopera.it

grabber.py 
- crawls GBOPERA site

parser.py 
- parses GBOPERA data, collects network statistics

transformer.py 
- transforms multi graphs into weighted graphs
    
analyzer.py
- calculates general network metrics, those of it's giant component
- plots network degree histogram, outputs list of nodes of highest degree
- compares metrics with those of Barbasi-Albert and Erdős–Rényi graphs

NetworkX library is used

cliques_spy.py 
- discovers opera singer cliques
- calculates operanetwork radius and diameter
- finds network center and finds nodes with high betweennes centrality
- and plots their ego graphs<br />
NetworkX library is used
      
community_spy.py
- applies Louvain community discovery method to opera network<br /> 
Library available here: http://perso.crans.org/aynaud/communities/ is used
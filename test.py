import npmi
from convectors.algorithms.pmi import pmi
import telekinesis as tlk
from convectors.layers import Tokenize
import time
from pprint import pprint
import networkx as nx
from louvain_numba import best_partition
from collections import Counter
import numpy as np

df = tlk.query(
    """
DATA { ~written_press~ }
TIMELINE { 30d }
INTENT { list->clean }
"""
).head(10000)
print(df)

documents = Tokenize(stopwords=["fr", "en", "es", "url"])(df["text"])
documents = [[it for it in doc if len(it) > 3][:128] for doc in documents]
count = Counter()
for doc in documents:
    count.update(doc)
print(len(documents))
print(count.most_common(10))

start = time.time()
npmi = npmi.calculate_npmi(documents, window_size=15, minimum_pmi=0.5, min_count=10)
print(time.time() - start)

start = time.time()
pmi(documents, window_size=15, min_count=10, minimum_pmi=0.5)
print(time.time() - start)

# # transform into a graph
# edges = [(u, v, w) for (u, v), w in npmi.items()]
# G = nx.Graph()
# G.add_weighted_edges_from(edges)
# nodes = list(G.nodes())

# centrality = nx.pagerank(G)
# # print(count[nodes[i]])
# centrality = {node: p * count[node] for node, p in centrality.items()}
# # centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

# partition = best_partition(G)
# partition = {nodes[i]: p for i, p in partition.items()}
# cm2nodes = {}
# for node, cluster in partition.items():
#     if cluster not in cm2nodes:
#         cm2nodes[cluster] = []
#     cm2nodes[cluster].append((node, centrality[node]))
# cm2nodes = sorted(
#     cm2nodes.items(), key=lambda x: np.sum([v[1] for v in x[1]]), reverse=True
# )
# cm2nodes = [sorted(v, key=lambda x: x[1], reverse=True)[:10] for k, v in cm2nodes]
# pprint(cm2nodes)

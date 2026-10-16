import pickle
import osmnx as ox

# 1. Dataset load karo
G = ox.load_graphml("delhi_station_du.graphml")
print("Raw MultiDiGraph -> Nodes:", len(G.nodes), "Edges:", len(G.edges))

# 1b. Largest strongly connected component rakho (nayi lines)
n_before = len(G.nodes)
G = ox.truncate.largest_component(G, strongly=True)
print("Nodes hataye:", n_before - len(G.nodes))
print("After component -> Nodes:", len(G.nodes), "Edges:", len(G.edges))

# 2. Vertices: id -> (lat, lon)   (A* heuristic ke liye)
coords = {n: (float(d["y"]), float(d["x"])) for n, d in G.nodes(data=True)}

# 3. Parallel edges mein se sabse chhoti length rakho, self-loops hatao
best = {}
for u, v, d in G.edges(data=True):
    if u == v:
        continue
    w = float(d["length"])
    if (u, v) not in best or w < best[(u, v)]:
        best[(u, v)] = w

# 4. Adjacency list: node -> [(neighbour, weight), ...]
adj = {n: [] for n in coords}
for (u, v), w in best.items():
    adj[u].append((v, w))

# 5. Stats
V = len(adj)
E = sum(len(nbrs) for nbrs in adj.values())
avg_deg = E / V
max_deg = max(len(nbrs) for nbrs in adj.values())

print("Vertices:", V)
print("Edges (directed):", E)
print("Average degree:", round(avg_deg, 2))
print("Maximum degree:", max_deg)

# 6. Aage ke parts ke liye save karo
with open("graph.pkl", "wb") as f:
    pickle.dump((adj, coords), f)
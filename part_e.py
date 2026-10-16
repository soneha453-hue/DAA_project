import csv
import random
import time
from collections import deque

import networkx as nx   # sirf connected component ke liye, shortest path ke liye nahi

from part_c import adj, coords, dijkstra, nearest_node
from part_d import astar

SIZES = [1000, 2500, 5000, len(adj)]   # last = poora graph
NUM_PAIRS = 10                          # kam se kam 5 chahiye
SEED = 42

# 1. BFS order: centre se bahar ki taraf failta hua vertices ka order
def bfs_order(adj, start):
    seen = {start}
    order = [start]
    q = deque([start])
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if v not in seen:
                seen.add(v)
                order.append(v)
                q.append(v)
    return order

# 2. Sub-graph banao: pehle N vertices + largest strongly connected component
def build_subgraph(order, N):
    keep = set(order[:N])
    G = nx.DiGraph()
    G.add_nodes_from(keep)
    for u in keep:
        for v, _ in adj[u]:
            if v in keep:
                G.add_edge(u, v)
    largest = max(nx.strongly_connected_components(G), key=len)
    return {u: [(v, w) for v, w in adj[u] if v in largest] for u in largest}

# 3. Start vertex: station aur DU ke beech ka centre
start = nearest_node((28.6431 + 28.6879) / 2, (77.2197 + 77.2100) / 2)
order = bfs_order(adj, start)

# 4. Experiments
def mean(xs):
    return sum(xs) / len(xs)

rows = []
for N in SIZES:
    sub = build_subgraph(order, N)
    V = len(sub)
    E = sum(len(n) for n in sub.values())

    nodes = sorted(sub)
    rng = random.Random(SEED)
    pairs = [tuple(rng.sample(nodes, 2)) for _ in range(NUM_PAIRS)]

    res = {"Dijkstra": [], "A*": []}
    for S, D in pairs:
        t0 = time.perf_counter()
        dc, _, dex, ded = dijkstra(sub, S, D)
        dt = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        ac, _, aex, aed = astar(sub, coords, S, D)
        at = (time.perf_counter() - t0) * 1000

        if abs(dc - ac) > 1e-6:
            print("WARNING: cost mismatch", S, D, dc, ac)

        res["Dijkstra"].append((dc, dex, ded, dt))
        res["A*"].append((ac, aex, aed, at))

    for algo in ("Dijkstra", "A*"):
        r = res[algo]
        rows.append({
            "Graph Size": V,
            "Edges": E,
            "Algorithm": algo,
            "Cost (m)": round(mean([x[0] for x in r]), 2),
            "Vertices Explored": round(mean([x[1] for x in r]), 1),
            "Edges Examined": round(mean([x[2] for x in r]), 1),
            "Time (ms)": round(mean([x[3] for x in r]), 3),
        })

# 5. Table print (README mein paste karne layak) + CSV save
cols = list(rows[0].keys())
print("| " + " | ".join(cols) + " |")
print("|" + "---|" * len(cols))
for r in rows:
    print("| " + " | ".join(str(r[c]) for c in cols) + " |")

with open("results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

print("\nPairs per size:", NUM_PAIRS, "| seed:", SEED)
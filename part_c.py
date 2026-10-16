import pickle
import heapq
import math
import time

# 1. Graph load
with open("graph.pkl", "rb") as f:
    adj, coords = pickle.load(f)

# 2. Haversine (meters), for nearest node 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def nearest_node(lat, lon):
    return min(coords, key=lambda n: haversine(lat, lon, coords[n][0], coords[n][1]))

# 3. Dijkstra
def dijkstra(adj, S, D):
    dist = {S: 0.0}
    parent = {S: None}
    done = set()                 # finalize  vertices
    heap = [(0.0, S)]
    edges_examined = 0

    while heap:
        d, u = heapq.heappop(heap)
        if u in done:            # old (stale) entry, skip
            continue
        done.add(u)
        if u == D:               # found destination 
            break
        for v, w in adj[u]:
            edges_examined += 1
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    if D not in done:            # disconnected case
        return None, None, len(done), edges_examined
    return dist[D], parent, len(done), edges_examined

# 4. Path reconstruction: D to S 
def build_path(parent, S, D):
    path = []
    cur = D
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

# 5. Run
if __name__ == "__main__":
    S = nearest_node(28.6431, 77.2197)   # New Delhi Railway Station
    D = nearest_node(28.6879, 77.2100)   # Delhi University North Campus
    print("S node:", S, coords[S])
    print("D node:", D, coords[D])

    t0 = time.perf_counter()
    cost, parent, explored, examined = dijkstra(adj, S, D)
    t1 = time.perf_counter()

    if cost is None:
        print("No path found (S aur D disconnected hain)")
    else:
        path = build_path(parent, S, D)
        print("Shortest-path cost (m):", round(cost, 2))
        print("Path vertices count:", len(path))
        print("Path:", path)
        print("Vertices explored:", explored)
        print("Edges examined:", examined)
        print("Execution time (ms):", round((t1 - t0) * 1000, 3))
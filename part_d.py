import heapq
import time
from part_c import adj, coords, haversine, nearest_node, build_path, dijkstra

def astar(adj, coords, S, D):
    dlat, dlon = coords[D]
    h = lambda n: haversine(coords[n][0], coords[n][1], dlat, dlon)

    g = {S: 0.0}
    parent = {S: None}
    done = set()
    heap = [(h(S), S)]            # (f, node), f = g + h
    edges_examined = 0

    while heap:
        f, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == D:
            break
        for v, w in adj[u]:
            edges_examined += 1
            ng = g[u] + w
            if v not in g or ng < g[v]:
                g[v] = ng
                parent[v] = u
                heapq.heappush(heap, (ng + h(v), v))

    if D not in done:
        return None, None, len(done), edges_examined
    return g[D], parent, len(done), edges_examined

if __name__ == "__main__":
    S = nearest_node(28.6431, 77.2197)
    D = nearest_node(28.6879, 77.2100)

    t0 = time.perf_counter()
    cost, parent, explored, examined = astar(adj, coords, S, D)
    t1 = time.perf_counter()

    if cost is None:
        print("No path found")
    else:
        path = build_path(parent, S, D)
        print("A* cost (m):", round(cost, 2))
        print("Path vertices count:", len(path))
        print("Vertices explored:", explored)
        print("Edges examined:", examined)
        print("Execution time (ms):", round((t1 - t0) * 1000, 3))

    # Dijkstra se comparison
    dc, _, dex, ded = dijkstra(adj, S, D)
    print("Dijkstra cost (m):", round(dc, 2), "| explored:", dex, "| examined:", ded)
    print("Same cost?", abs(cost - dc) < 1e-6)
import csv
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from part_c import adj, coords, dijkstra, build_path, nearest_node

# ---------- Part 1: results.csv se comparison graphs ----------
with open("results.csv") as f:
    rows = list(csv.DictReader(f))

sizes = [int(r["Graph Size"]) for r in rows if r["Algorithm"] == "Dijkstra"]

def series(algo, col):
    return [float(r[col]) for r in rows if r["Algorithm"] == algo]

def compare_plot(col, ylabel, title, fname):
    plt.figure(figsize=(6, 4))
    plt.plot(sizes, series("Dijkstra", col), "o-", label="Dijkstra")
    plt.plot(sizes, series("A*", col), "s-", label="A*")
    plt.xlabel("Graph size (vertices)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fname, dpi=200)
    plt.close()

compare_plot("Vertices Explored", "Vertices explored (avg)",
             "Vertices explored vs graph size", "plot_vertices.png")
compare_plot("Edges Examined", "Edges examined (avg)",
             "Edges examined vs graph size", "plot_edges.png")
compare_plot("Time (ms)", "Execution time in ms (avg)",
             "Execution time vs graph size", "plot_time.png")

# ---------- Part 2: Station to DU route map ----------
S = nearest_node(28.6431, 77.2197)
D = nearest_node(28.6879, 77.2100)
cost, parent, _, _ = dijkstra(adj, S, D)
path = build_path(parent, S, D)

# saari roads halke grey mein (x = longitude, y = latitude)
segments = []
for u, nbrs in adj.items():
    for v, _ in nbrs:
        segments.append([(coords[u][1], coords[u][0]),
                         (coords[v][1], coords[v][0])])

fig, ax = plt.subplots(figsize=(7, 8))
ax.add_collection(LineCollection(segments, colors="lightgrey", linewidths=0.4))

px = [coords[n][1] for n in path]
py = [coords[n][0] for n in path]
ax.plot(px, py, color="red", linewidth=2, label=f"Shortest path ({cost/1000:.2f} km)")
ax.scatter(px[0], py[0], c="green", s=60, zorder=3, label="Station (S)")
ax.scatter(px[-1], py[-1], c="blue", s=60, zorder=3, label="Delhi University (D)")

ax.autoscale()
ax.set_aspect("equal")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title("Shortest route: New Delhi Station to Delhi University")
ax.legend()
plt.tight_layout()
plt.savefig("plot_route.png", dpi=200)
plt.close()

print("Saved: plot_vertices.png, plot_edges.png, plot_time.png, plot_route.png")
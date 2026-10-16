import osmnx as ox

# bbox = (west, south, east, north)
bbox = (77.18, 28.63, 77.25, 28.70)

G = ox.graph_from_bbox(bbox, network_type="drive")
ox.save_graphml(G, "delhi_station_du.graphml")

print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))
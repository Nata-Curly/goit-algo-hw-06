import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from collections import defaultdict


G = nx.Graph()

G.add_nodes_from(
    ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Nik", "Natalia"]
)

G.add_edge("Alice", "Bob", weight=9)
G.add_edge("Alice", "Charlie", weight=5)
G.add_edge("Alice", "Frank", weight=3)
G.add_edge("Alice", "David", weight=5)
G.add_edge("Alice", "Emma", weight=3)
G.add_edge("Bob", "David", weight=4)
G.add_edge("Bob", "Nik", weight=4)
G.add_edge("Bob", "Natalia", weight=5)
G.add_edge("Charlie", "David", weight=3)
G.add_edge("Charlie", "Emma", weight=1)
G.add_edge("David", "Emma", weight=2)
G.add_edge("David", "Frank", weight=5)
G.add_edge("Emma", "Frank", weight=6)
G.add_edge("Frank", "Charlie", weight=3)
G.add_edge("Nik", "Natalia", weight=7)
G.add_edge("Nik", "Charlie", weight=8)
G.add_edge("Nik", "Alice", weight=3)
G.add_edge("Natalia", "Alice", weight=7)


pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, "weight")
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=800,
    node_color="skyblue",
    edge_color="darkblue",
    font_size=10,
    font_weight="bold",
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Моделювання соціальної мережі")
plt.show()

print("Кількість вузлів: ", G.number_of_nodes())
print("Кількість ребер: ", G.number_of_edges())
print("Ступінь центральності: ", nx.degree_centrality(G))
print("Близькість вузла: ", nx.closeness_centrality(G))
print("Посередництво вузла: ", nx.betweenness_centrality(G))


def dfs_recursive(G, vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(vertex)
    print(vertex, end=" ")
    for neighbor in G[vertex]:
        if neighbor not in visited:
            dfs_recursive(G, neighbor, visited)


def bfs_recursive(graph, queue, visited=None):
    if visited is None:
        visited = set()
    if not queue:
        return
    vertex = queue.popleft()
    if vertex not in visited:
        print(vertex, end=" ")
        visited.add(vertex)
        queue.extend(set(graph[vertex]) - visited)
    bfs_recursive(graph, queue, visited)


print("\nDFS recursive:")
dfs_recursive(G, "Alice")

print("\nBFS recursive:")
bfs_recursive(G, deque(["Alice"]))


def dijkstra(graph, start):
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    visited = set()
    paths = defaultdict(list)

    while len(visited) < len(graph):
        current_vertex = min(
            (vertex for vertex in graph if vertex not in visited),
            key=lambda vertex: distances[vertex],
        )
        visited.add(current_vertex)
        for neighbor, data in graph[current_vertex].items():
            weight = data["weight"]
            if distances[current_vertex] + weight < distances[neighbor]:
                distances[neighbor] = distances[current_vertex] + weight
                paths[neighbor] = paths[current_vertex] + [current_vertex]

    return distances, paths


distances, paths = dijkstra(dict(G.adj), "Alice")

print("\n")
print("-" * 50)
print("\nНайкоротші відстані:")
for vertex, distance in distances.items():
    print(f"{vertex}: {distance}")

print("\nНайкоротші шляхи:")
for vertex, path in paths.items():
    print(f"{vertex}: {' -> '.join(path + [vertex])}")

all_shortest_paths = dict(nx.all_pairs_shortest_path(G))
print("\nНайкоротші шляхи між усіма вершинами:")
for source, paths in all_shortest_paths.items():
    for target, path in paths.items():
        if source != target:
            print(f"{source} -> {target}: {' -> '.join(path)}")

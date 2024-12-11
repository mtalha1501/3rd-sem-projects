import heapq

def dijkstra(graph, start, end):
    # Priority queue for the minimum cost path
    pq = []
    heapq.heappush(pq, (0, start))  # (cost, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return distances[end], path

# Graph representation: adjacency list
graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('C', 6), ('D', 1)],
    'C': [('A', 5), ('B', 6), ('D', 2)],
    'D': [('B', 1), ('C', 2), ('E', 1)],
    'E': [('D', 1)]
}

def main():
    print("Travel Planner")
    print("Nodes available: A, B, C, D, E")

    start = input("Enter start location: ").strip().upper()
    end = input("Enter destination: ").strip().upper()

    if start not in graph or end not in graph:
        print("Invalid locations entered.")
        return

    distance, path = dijkstra(graph, start, end)

    if distance == float('inf'):
        print(f"No path found from {start} to {end}.")
    else:
        print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
        print(f"Total cost: {distance}")

if __name__ == "__main__":
    main()

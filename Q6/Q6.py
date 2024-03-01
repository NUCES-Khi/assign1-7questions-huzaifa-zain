from collections import deque
from queue import PriorityQueue

heuristics = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

map_graph = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101}
}


def bfs_traversal(graph, start, end):
    visited = set()
    queue = deque([[start]])
    if start == end:
        return [start]
    while queue:
        path = queue.popleft()
        current_node = path[-1]
        if current_node not in visited:
            neighbors = graph[current_node]
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == end:
                    return new_path
            visited.add(current_node)
    return None


def uniform_cost(graph, start, end):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, [start]))
    while not priority_queue.empty():
        cost, path = priority_queue.get()
        current_node = path[-1]
        if current_node not in visited:
            if current_node == end:
                return path
            visited.add(current_node)
            neighbors = graph[current_node]
            for neighbor, weight in neighbors.items():
                if neighbor not in visited:
                    total_cost = cost + weight
                    new_path = list(path)
                    new_path.append(neighbor)
                    priority_queue.put((total_cost, new_path))
    return None


def greedy_best_first(graph, start, end, heuristic):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((heuristic[start], [start]))
    while not priority_queue.empty():
        _, path = priority_queue.get()
        current_node = path[-1]
        if current_node not in visited:
            visited.add(current_node)
            if current_node == end:
                return path
            for neighbor, _ in graph[current_node].items():
                if neighbor not in visited:
                    priority_queue.put((heuristic[neighbor], path + [neighbor]))
    return None


def iterative_deepening_dfs(graph, start, end):
    depth_limit = 0
    while True:
        stack = [(start, [start])]
        visited = set()
        while stack:
            current_node, path = stack.pop()
            if current_node == end:
                return path
            if len(path) <= depth_limit:
                if current_node not in visited:
                    visited.add(current_node)
                    for neighbor in graph[current_node]:
                        if neighbor not in visited:
                            stack.append((neighbor, path + [neighbor]))
        depth_limit += 1


def calculate_cost(path, graph):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i + 1]]
    return total_cost


start_point = input("Enter Starting Location: ")
destination_point = input("Enter Destination: ")
if start_point not in map_graph or destination_point not in map_graph:
    print("Invalid Input")
else:
    bfs_path = bfs_traversal(map_graph, start_point, destination_point)
    if bfs_path:
        bfs_cost = calculate_cost(bfs_path, map_graph)
        print("Shortest Path by Breadth-First Search: {}. Cost by Breadth-First Search: {}".format(bfs_path, bfs_cost))
    else:
        print("No Path Found")
    ucs_path = uniform_cost(map_graph, start_point, destination_point)
    if ucs_path:
        ucs_cost = calculate_cost(ucs_path, map_graph)
        print("Shortest Path by Uniform Cost Search: {}. Cost by Uniform Cost Search: {}".format(ucs_path, ucs_cost))
    else:
        print("No Path Found")
    gbfs_path = greedy_best_first(map_graph, start_point, destination_point, heuristics)
    if gbfs_path:
        gbfs_cost = calculate_cost(gbfs_path, map_graph)
        print("Shortest Path by Greedy Best First Search: {}. Cost by Greedy Best First Search: {}".format(gbfs_path, gbfs_cost))
    else:
        print("No Path Found")
    iddfs_path = iterative_deepening_dfs(map_graph, start_point, destination_point)
    if iddfs_path:
        iddfs_cost = calculate_cost(iddfs_path, map_graph)
        print("Shortest Path by Iterative Deepening Depth-First Search: {}. Cost by Iterative Deepening Depth-First Search: {}".format(iddfs_path, iddfs_cost))
    else:
        print("No Path Found")
    sorted_algorithms = sorted([
        ("Breadth-First Search", bfs_cost),
        ("Uniform Cost Search", ucs_cost),
        ("Greedy Best-First Search", gbfs_cost),
        ("Iterative Deepening Depth-First Search", iddfs_cost)
    ], key=lambda x: x[1])
    print("\nShortest Path Algorithms (Ascending Order):")
    for algorithm, cost in sorted_algorithms:
        print("{}: Cost {}".format(algorithm, cost))

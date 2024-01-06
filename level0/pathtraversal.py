import json

def tsp(graph, start):
    nodes = list(graph.keys())
    nodes.remove(start)

    path = [start]
    current_node = start

    while nodes:
        nearest_neighbor = min(nodes, key=lambda node: graph[current_node][node])
        path.append(nearest_neighbor)
        current_node = nearest_neighbor
        nodes.remove(nearest_neighbor)

    path.append(start)
    distance = sum(graph[path[i]][path[i+1]] for i in range(len(path) - 1))

    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue
                new_path = path[:]
                new_path[i:j] = path[j - 1:i - 1:-1]
                new_distance = sum(graph[new_path[k]][new_path[k + 1]] for k in range(len(new_path) - 1))
                if new_distance < distance:
                    path = new_path
                    distance = new_distance
                    improved = True

    return path, distance


with open('level0/level0.json', 'r') as f:
    data = json.load(f)

distance = {}

neighbours = ['n' + str(i) for i in range(20)]
vehicle = list(data['vehicles'].keys())[0]
if 'restaurants' in data:
    for k, v in data['restaurants'].items():
        distance[k] = {neighbours[i]: weight for i, weight in enumerate(v['neighbourhood_distance'])}
        distance[k]['r0'] = 0

for k, v in data['neighbourhoods'].items():
    distance[k] = {neighbours[i]: weight for i, weight in enumerate(v['distances'])}
    v['order_']
    distance[k]['r0'] = distance['r0'][k]


start = list(data['vehicles'].values())[0]['start_point']
path, distance = tsp(distance, start)
formatted_path = {vehicle: {"path": path}}

output_file = 'level0/level0_output.json'

with open(output_file, 'w') as f:
    json.dump(formatted_path, f)

print(f"Output saved to {output_file}")

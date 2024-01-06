import json

def optimize(graph,path):
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
    return path
def tsp(distances, order_sizes, start, capacity):
    nodes = list(distances.keys())
    nodes.remove(start)
    paths = []
    current_path = [start]
    current_capacity = 0
    current_node = start

    while nodes:
        nearest_neighbor = min(nodes, key=lambda node: distances[current_node][node])
        if current_capacity + order_sizes[nearest_neighbor] > capacity:
            current_path = optimize(distances,current_path)
            if(len(current_path)>1):
                current_path.append(start)
                paths.append(current_path)
            current_path = [start]
            current_capacity = 0
        else:
            current_path.append(nearest_neighbor)
            current_capacity += order_sizes[nearest_neighbor]
            nodes.remove(nearest_neighbor)

    if len(current_path) > 1:
        current_path.append(start)
        paths.append(current_path)

    return paths


with open('level1b/level1b.json', 'r') as f:
    data = json.load(f)

distance = {}

neighbours = ['n' + str(i) for i in range(50)]
cost_capacity = {}
vehicle = list(data['vehicles'].keys())[0]
if 'restaurants' in data:
    for k, v in data['restaurants'].items():
        distance[k] = {neighbours[i]: weight for i, weight in enumerate(v['neighbourhood_distance'])}
        distance[k]['r0']= 0

for k, v in data['neighbourhoods'].items():
    distance[k] = {neighbours[i]: weight for i, weight in enumerate(v['distances'])}
    cost_capacity[k] = v['order_quantity']
    distance[k]['r0'] = distance['r0'][k]

start = list(data['vehicles'].values())[0]['start_point']
capacity = list(data['vehicles'].values())[0]['capacity']
paths= tsp(distance,cost_capacity, start,capacity)
formatted_path = {vehicle: {"path"+f"{i}": paths[i-1] for i in range(1,len(paths)+1)}}
print(formatted_path)
output_file = 'level1b/level1b_output.json'

with open(output_file, 'w') as f:
    json.dump(formatted_path, f)

print(f"Output saved to {output_file}")


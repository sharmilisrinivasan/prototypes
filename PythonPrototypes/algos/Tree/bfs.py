def process(ele):
	print(f"{ele} => ")

def bfs(my_graph, start_node):

	visited = set()
	queue = [start_node]

	while queue:
		ele = queue.pop(0)

		if ele in visited:
			continue

		visited.add(ele)
		process(ele)

		for child in my_graph.get(ele,[]):
			queue.append(child)

def bfs_new(my_graph, start_node):

	visited = set(start_node)
	queue = [start_node]

	while queue:
		ele = queue.pop(0)
		process(ele)

		for child in my_graph.get(ele,[]):
			if child not in visited:
				visited.add(child)
				queue.append(child)

if __name__ == '__main__':
	my_graph = {
		"1": ["2", "3"],
		"2": ["1","3"],
		"3": ["1", "2", "4", "5", "6"],
		"4": ["3", "5"],
		"5": ["3", "4"],
		"6": ["3"]
	}

	# my_graph = {
	# 	"1": ["2", "3"],
	# 	"2": ["4","5"],
	# 	"3": ["6", "7"]
	# }

	bfs_new(my_graph, "1")

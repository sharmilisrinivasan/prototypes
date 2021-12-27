def process(ele):
	print(f"{ele} => ")

def dfs_iterative(my_graph, start_node):

	if start_node in my_graph:
		stack = [start_node]
	else:
		raise("Start node wrong")

	visited = set()

	while stack:
		ele = stack.pop()
		if ele in visited:
			continue
		
		visited.add(ele)	
		
		process(ele)
		for child in my_graph.get(ele,[]):
			stack.append(child)

def dfs_iterative_new(my_graph, start_node):

	visited = set(start_node)
	stack = [start_node]

	while stack:
		ele = stack.pop()
		process(ele)	
		
		for child in my_graph.get(ele,[]):
			if child not in visited:
				visited.add(child)
				stack.append(child)

def dfs_recursive(my_graph, start_node, visited=None):
	if not visited:
		visited = set()

	if start_node in visited:
		return

	visited.add(start_node)
	process(start_node)

	for child in my_graph.get(start_node,[]):
		dfs_recursive(my_graph, child, visited)


def dfs_recursive_new(my_graph, start_node, visited=None):
	if visited is None:
		visited = set(start_node)

	process(start_node)

	for child in my_graph.get(start_node,[]):
		if child not in visited:
			visited.add(child)
			dfs_recursive_new(my_graph, child, visited)


if __name__ == '__main__':
	# my_graph = {
	# 	"1": ["2", "3"],
	# 	"2": ["1","3"],
	# 	"3": ["1", "2", "4", "5", "6"],
	# 	"4": ["3", "5"],
	# 	"5": ["3", "4"],
	# 	"6": ["3"]
	# }

	my_graph = {
		"1": ["2", "3"],
		"2": ["4","5"],
		"3": ["6", "7"]
	}

	# dfs_iterative(my_graph, "1")
	# dfs_recursive(my_graph, "1")
	# dfs_iterative_new(my_graph, "1")
	dfs_recursive_new(my_graph, "1")

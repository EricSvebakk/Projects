import graphviz
import os

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

# =============================================
class Vertex:
	def __init__(self, elem):
		self.elem = f"{elem}"
		self.ni = set()
		self.tuo = dict()
	
	def __repr__(self) -> str:
		return self.elem

def edge(node1, node2, status):
	node1.ni.add(node2)
	node2.tuo[node1] = status
	# node2.tuo.add(node1)

# =============================================
def buildgraph(lines):
	graph = dict()
	
	for line in lines:
		course, *prereqs = line.strip().split()
		graph[course] = Vertex(course)
		
		for prereq in prereqs:
			prereq = prereq.replace("*", "")
			graph[prereq] = Vertex(prereq)
			
	
	for line in lines:
		course, *prereqs = line.strip().split()
		v = graph[course]

		for prereq in prereqs:

			w = graph[prereq.replace("*","")]
			edge(v,w,"*" in prereq)
			
	# print("===========================")
	# for key in graph:
		# print(f"{key}: {graph[key]} ",end="")
		# for elem in graph[key].tuo:
			# print(f" {elem}(", end="")
			# if graph[key].tuo[elem]:
				# print("T)", end="")
			# else:
				# print("F)", end="")
		# print("")
	# print("===========================")
	
	return graph

# =============================================
# def topsort(graph):
# 	V = graph.values()
# 	stack = []
# 	result = []
	
# 	for v in V:
# 		if (len(v.ni)) == 0:
# 			stack.append(v)
			
# 	while len(stack) > 0:
# 		v = stack.pop()
# 		result.append(v.elem)
		
# 		for w in v.tuo:
# 			w.ni.discard(v)
			
# 			if len(w.ni) == 0:
# 				stack.append(w)
				
# 	return result
		
# =============================================
def drawgraph(gDict):
	dot = graphviz.Digraph()
	
	for key in gDict:
		dot.node(key)
		
		
	for key in gDict:
		for vertex in gDict[key].tuo:
			# print(key, vertex, gDict[key].tuo[vertex], type(key), type(vertex))
			
			if gDict[key].tuo[vertex]:
				dot.edge(key, vertex.elem, color="green")
			else:
				dot.edge(key, vertex.elem, color="red")
				
	
	dot.render("sub-prereq-graph", format="svg", view=True)
	
# =============================================
with open("sub-prereq-scrape", "r") as f:
	lines = f.readlines()
		
	graph = buildgraph(lines)
	
	# for key in graph:
	# 	if len(graph[key].tuo) != 0:
	# 		print(f"{key} {graph[key].tuo}")
	# 	else:
	# 		print(f"{key}")

	drawgraph(graph)
	
	# print(topsort(graph))

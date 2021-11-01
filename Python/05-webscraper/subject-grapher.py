import graphviz
import os

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
file_name = "uio_subjects"


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
	
	dot.render(f"{file_name}_graph", format="svg", view=True)


# =============================================
with open(file_name, "r") as file:
	
	graph = buildgraph(file.readlines())
	
	# for key in graph:
	# 	if len(graph[key].tuo) != 0:
	# 		print(f"{key} {graph[key].tuo}")
	# 	else:
	# 		print(f"{key}")

	drawgraph(graph)

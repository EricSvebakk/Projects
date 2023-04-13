import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;

//
class Data {
	/**
	 *
	 */
	private final Graph graph;

	/**
	 * @param graph
	 */
	Data(Graph graph) {
		this.graph = graph;
	}

	HashMap<Integer, Integer> components = new HashMap<>();
	HashMap<Node, Boolean> visited = new HashMap<>();
	HashMap<Node, Node> parents = new HashMap<>();

	HashMap<String, Node> nodes = new HashMap<>();
	HashMap<String, Edge> edges = new HashMap<>();

	//
	public void addNode(String id, Node node) {
		nodes.put(id, node);
		visited.put(node, false);
	}

	public void addEdge(String id, Edge edge) {
		edges.put(id, edge);
	}

	// public void addNodeToEdge(String nmid, String ttid) {
	// 	if (edges.containsKey(ttid)) {
	// 		Edge edge = edges.get(ttid);
	// 		Node node = nodes.get(nmid);

	// 		// if (!edge.nodes.contains(node)) {
	// 		// 	edge.nodes.add(node);
	// 		// }
	// 	}
	// }

	public void addParent(Node child, Node parent) {
		parents.put(child, parent);
	}

	//
	public void addComponent(int key) {
		if (components.containsKey(key)) {
			components.replace(key, components.get(key) + 1);
		} else {
			components.put(key, 1);
		}
	}

	//
	public Collection<Node> getNodes() {
		return nodes.values();
	}

	public Collection<Edge> getEdges() {
		return edges.values();
	}

	public Node getParent(Node child) {
		return parents.get(child);
	}

	//
	public void printComponents() {
		
		Integer[] temp = (Integer[]) components.keySet().toArray(new Integer[components.keySet().size()]);
		Arrays.sort(temp);
		
		for (Integer n : temp) {
			System.out.println(components.get(n) + " groups of size " + n);
		}
		
		System.out.println();
	}

	//
	public void startVisit() {
		for (Node n : nodes.values()) {
			visited.replace(n, false);
			n.dValue = 999999999;
		}
		parents.clear();
		components.clear();
	}

	public void visit(Node node) {
		visited.replace(node, true);
	}

	public boolean hasVisited(Node node) {
		return visited.get(node);
	}

	public boolean hasComponent(int key) {
		return components.containsKey(key);
	}

}
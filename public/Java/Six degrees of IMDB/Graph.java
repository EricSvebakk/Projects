import java.io.File;
import java.io.FileNotFoundException;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.Stack;

class Graph {

	//
	class Node implements Comparable<Node> {
		HashMap<Node, Edge> nodes = null;
		HashSet<Edge> edges = null;
		String nmid;
		String name;
		double dValue = 0;

		public Node(String nmid, String name) {
			this.nmid = nmid;
			this.name = name;
			this.nodes = new HashMap<>();
			this.edges = new HashSet<>();
		}

		public void addRelation(Node other, Edge edge) {
			if (nodes.containsKey(other)) {
				if (edge.rating > nodes.get(other).rating) {
					nodes.put(other, edge);
					edges.add(edge);
				}
			} else {
				nodes.put(other, edge);
				edges.add(edge);
			}
		}

		@Override
		public String toString() {
			return "(" + nmid + "|" + name + "|" + nodes.size() + ")";
		}

		@Override
		public int compareTo(Node n) {
			return Double.compare(this.dValue, n.dValue);
		}
	}

	//
	class Edge {
		HashSet<Node> nodes;
		String ttid;
		String title;
		double rating;

		public Edge(String ttid, String title, double rating) {
			this.ttid = ttid;
			this.title = title;
			this.rating = rating;
			this.nodes = new HashSet<>();
		}

		public Edge(Edge edge) {
			this.ttid = edge.ttid;
			this.title = edge.title;
			this.rating = edge.rating;
			this.nodes = new HashSet<>(edge.nodes);
		}

		@Override
		public String toString() {
			return "[" + ttid + "|" + title + "|" + rating + "]";
		}
	}

	//
	class Data {
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

		public void addNodeToEdge(String nmid, String ttid) {
			if (edges.containsKey(ttid)) {
				Edge edge = edges.get(ttid);
				Node node = nodes.get(nmid);

				if (!edge.nodes.contains(node)) {
					edge.nodes.add(node);
				}
			}
		}

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
			for (int n : data.components.keySet()) {
				System.out.println("Size " + n + ": " + components.get(n));
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

	Data data;

	public Graph(File fileNodes, File fileEdges) {

		Scanner scannerNode = null;
		Scanner scannerEdge = null;

		try {
			scannerNode = new Scanner(fileNodes);
			scannerEdge = new Scanner(fileEdges);
		}

		catch (FileNotFoundException e) {
			if (scannerNode == null) {
				System.out.println("Fil '" + fileEdges + "' ikke funnet!");
			} else {
				System.out.println("Fil '" + fileNodes + "' ikke funnet!");
			}
			return;
		}

		this.data = new Data();

		while (scannerEdge.hasNextLine()) {

			String[] words = scannerEdge.nextLine().split("\t");
			String ttid = words[0].strip();
			String title = words[1].strip();
			double rating = Double.parseDouble(words[2]);

			data.addEdge(ttid, new Edge(ttid, title, rating));
		}

		while (scannerNode.hasNextLine()) {

			String[] bits = scannerNode.nextLine().split("\t");
			String nmid = bits[0].strip();
			String name = bits[1].strip();

			data.addNode(nmid, new Node(nmid, name));

			for (int i = 2; i < bits.length; i++) {
				data.addNodeToEdge(nmid, bits[i]);
			}
		}

		scannerNode.close();
		scannerEdge.close();
	}

	public void createGraph() {

		int index = 0;

		for (Edge edge : data.getEdges()) {
			Edge edgeTemp = new Edge(edge);

			for (Node node1 : edge.nodes) {
				edgeTemp.nodes.remove(node1);

				for (Node node2 : edgeTemp.nodes) {

					if (!node1.equals(node2)) {
						node1.addRelation(node2, edge);
						node2.addRelation(node1, edge);
						index += 1;
					} else {
						System.out.println(node1 + " " + node2);
						return;
					}
				}
			}
		}

		System.out.println("Nodes: " + data.nodes.size());
		System.out.println("Edges: " + index + "\n");
	}

	public void shortestPath(String startID, String endID) {

		Node startNode = data.nodes.get(startID);
		Node endNode = data.nodes.get(endID);

		if (startNode == null) {
			System.out.println("Startnode '" + startID + "' invalid!\n");
			return;
		}

		if (endNode == null) {
			System.out.println("Endnode '" + endID + "' invalid!\n");
			return;
		}

		data.startVisit();
		data.visit(endNode);

		Stack<Node> L0 = new Stack<>();
		L0.add(endNode);

		recursiveShortestPath(L0, startNode, endNode, 0, 1);
	}

	private void recursiveShortestPath(Stack<Node> L0, Node startNode, Node endNode, int i, int j) {

		if (j == 0) {
			System.out.println("No path found between " + startNode.name + " and " + endNode.name + "\n");
			return;
		}

		j = 0;

		Stack<Node> L1 = new Stack<>();

		out: while (L0.size() > 0) {
			Node parent = L0.pop();

			for (Node child : parent.nodes.keySet()) {

				if (!data.hasVisited(child)) {
					L1.add(child);
					data.visit(child);
					data.addParent(child, parent);
				}
				j++;
			}
		}

		if (!L1.contains(startNode)) {
			recursiveShortestPath(L1, startNode, endNode, i, j);
		} else {
			pathPrint(startNode, endNode, true);
		}
	}

	public void chillestPath(String startID, String endID) {

		Node startNode = data.nodes.get(startID);
		Node endNode = data.nodes.get(endID);

		if (startNode == null) {
			System.out.println("Startnode '" + startID + "' invalid!\n");
			return;
		}

		if (endNode == null) {
			System.out.println("Endnode '" + endID + "' invalid!\n");
			return;
		}

		PriorityQueue<Node> queue = new PriorityQueue<>();

		data.startVisit();

		endNode.dValue = 0;
		queue.add(endNode);
		data.visit(endNode);

		while (queue.size() != 0) {

			Node parent = queue.poll();
			data.visit(parent);

			for (Node child : parent.nodes.keySet()) {

				double change = ((10 - parent.nodes.get(child).rating) + parent.dValue);

				if ((change < child.dValue) && !data.hasVisited(child)) {

					child.dValue = change;
					data.addParent(child, parent);

					queue.remove(child);
					queue.add(child);
				}
			}
		}

		pathPrint(startNode, endNode, true);
	}

	public void findComponents() {

		Stack<Node> remainder = new Stack<>();
		for (Node n : data.nodes.values()) {
			remainder.add(n);
		}

		data.startVisit();

		int i = 0;
		while (remainder.size() > 0) {

			Stack<Node> L0 = new Stack<>();
			Stack<Node> total = new Stack<>();

			Node node = remainder.pop();

			data.visit(node);
			total.add(node);

			L0.add(node);
			recFindComponents(L0, remainder, total, 0);

			data.addComponent(total.size());
		}

		data.printComponents();
	}

	private void recFindComponents(Stack<Node> L0, Stack<Node> remainder, Stack<Node> total, int i) {

		i = 0;

		Stack<Node> L1 = new Stack<>();

		out: while (L0.size() > 0) {
			Node parent = L0.pop();

			for (Node child : parent.nodes.keySet()) {

				if (!data.hasVisited(child)) {
					L1.add(child);
					data.visit(child);
					remainder.remove(child);
					total.add(child);
				}
				i++;
			}
		}

		if (i == 0) {
			return;
		}

		recFindComponents(L1, remainder, total, i);
	}

	private void pathPrint(Node startNode, Node endNode, Boolean weight) {

		Node node = startNode;
		String s = node.name;

		Node tempNode;
		Edge tempEdge;

		double totWeight = 0;
		double numEdges = 0;

		while (!node.equals(endNode)) {
			tempNode = data.getParent(node);
			tempEdge = tempNode.nodes.get(node);

			String pad = String.format("%" + (22 - tempNode.name.length()) + "s", "");
			s += "\n==> " + tempNode.name + pad;
			s += "| " + tempEdge.title + " (" + tempEdge.rating + ")";

			node = tempNode;

			numEdges += 10;
			totWeight += (tempEdge.rating);
		}

		System.out.println(s);

		if (weight) {
			String stringWeight = String.format("%.1f", numEdges - totWeight);
			System.out.println("W: " + stringWeight);
		}

		// System.out.println("\n" + "-".repeat(65));
		System.out.println();
	}
}
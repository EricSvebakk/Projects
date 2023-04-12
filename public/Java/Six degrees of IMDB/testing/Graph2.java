// package Obliger.Oblig2;

import java.util.Scanner;

import java.util.Stack;
import java.util.HashMap;
import java.util.HashSet;

import java.util.Comparator;
import java.util.PriorityQueue;

public class Graph2 {

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
			nodes.put(other, edge);
			edges.add(edge);
		}

		@Override
		public String toString() {
			return "(" + nmid + "|" + name + "|" + nodes.size() + ")";
		}

		@Override
		public int compareTo(Node n) {

			if (this.dValue == n.dValue) {
				return 0;
			}

			if (this.dValue > n.dValue) {
				return 1;
			} else {
				return -1;
			}
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

	HashMap<String, Node> nodes;
	HashMap<String, Edge> edges;

	HashMap<Node, Boolean> visited = new HashMap<>();
	HashMap<Node, Node> relatesTo = new HashMap<>();

	public Graph2(Scanner scannerEdge, Scanner scannerNode) {

		this.nodes = new HashMap<>();
		this.edges = new HashMap<>();

		String ttid;
		String title;
		double rating;
		Edge edge;
		for (String line = scannerEdge.nextLine();; line = scannerEdge.nextLine()) {
			String[] words = line.split("\t");
			ttid = words[0].strip();
			title = words[1].strip();
			rating = Double.parseDouble(words[2]);

			edge = new Edge(ttid, title, rating);
			edges.put(ttid, edge);

			if (!scannerEdge.hasNextLine()) {
				break;
			}
		}
		System.out.println("Edges finished.");

		String nmid;
		String name;
		Node node;
		for (String line = scannerNode.nextLine();; line = scannerNode.nextLine()) {
			String[] bits = line.split("\t");

			nmid = bits[0].strip();
			name = bits[1].strip();
			node = new Node(nmid, name);

			for (int i = 2; i < bits.length; i++) {

				if (edges.containsKey(bits[i])) {
					if (!edges.get(bits[i]).nodes.contains(node)) {
						edges.get(bits[i]).nodes.add(node);
					}
				}
			}

			nodes.put(nmid, node);

			if (!scannerNode.hasNextLine()) {
				break;
			}
		}
		System.out.println("Nodes finished.");

	}

	public void createGraph() {

		int index = 0;

		for (Edge edge : edges.values()) {
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

		System.out.println("Nodes: " + nodes.size());
		System.out.println("Edges: " + index + " " + "\n");
	}

	public void widthFirstSearch(Node startNode, Node endNode) {

		if (startNode == null) {
			System.out.println("Startnode invalid!\n");
			return;
		}

		if (endNode == null) {
			System.out.println("Endnode invalid!\n");
			return;
		}

		visited.clear();
		relatesTo.clear();
		for (Node node : nodes.values()) {
			visited.put(node, false);
		}
		visited.put(endNode, true);

		Stack<Node> L0 = new Stack<>();
		L0.add(endNode);

		WFSRecursive(L0, endNode, startNode, 0, 1);
	}

	public void WFSRecursive(Stack<Node> L0, Node startNode, Node endNode, int i, int j) {

		if (j == 0) {
			System.out.println("No path found between " + endNode.name + " and " + startNode.name + "\n");
			return;
		}

		j = 0;

		Stack<Node> L1 = new Stack<>();

		out: while (L0.size() > 0) {
			Node node1 = L0.pop();

			for (Node node2 : node1.nodes.keySet()) {

				if (!visited.get(node2)) {
					L1.add(node2);
					visited.replace(node2, true);
					relatesTo.put(node2, node1);
				}
				j++;
			}
		}

		if (!L1.contains(endNode)) {
			WFSRecursive(L1, startNode, endNode, i, j);
		}

		else {
			Node node = endNode;
			Edge tempEdge;
			Node tempNode;
			String s = node.name;

			while (!node.equals(startNode)) {
				tempNode = relatesTo.get(node);
				tempEdge = tempNode.nodes.get(node);

				String pad = String.format("%" + (23 - tempNode.name.length()) + "s", "");
				s += "\n--> " + tempNode.name + pad;
				s += "[ " + tempEdge.title + " (" + tempEdge.rating + ") ]";

				node = tempNode;
			}

			System.out.println(s + "\n\n" + "-".repeat(60) + "\n");
		}
	}

	public void dijkstra(Node startNode, Node endNode) {

		visited.clear();
		relatesTo.clear();
		PriorityQueue<Node> queue = new PriorityQueue<>();

		for (Node node : nodes.values()) {
			node.dValue = 999999999;
			visited.put(node, false);
		}

		endNode.dValue = 0;
		queue.add(endNode);
		visited.put(endNode, true);

		while (queue.size() != 0) {

			Node temp = queue.poll();
			visited.replace(temp, true);

			for (Node nNode : temp.nodes.keySet()) {

				double change = ((10 - temp.nodes.get(nNode).rating) + temp.dValue);

				if ((change < nNode.dValue) && !visited.get(nNode)) {

					nNode.dValue = change;
					relatesTo.put(nNode, temp);

					queue.remove(nNode);
					queue.add(nNode);
				}
			}
		}

		Node node = startNode;
		String s = node.name;

		Edge tempEdge;
		Node tempNode;

		double totWeight = 0;
		double numEdges = 0;

		while (!node.equals(endNode)) {
			tempNode = relatesTo.get(node);
			tempEdge = tempNode.nodes.get(node);

			String pad = String.format("%" + (23 - tempNode.name.length()) + "s", "");
			s += "\n--> " + tempNode.name + pad;
			s += "[ " + tempEdge.title + " (" + tempEdge.rating + ") ]";

			node = tempNode;

			numEdges += 10;
			totWeight += (tempEdge.rating);
		}

		System.out.println(s);
		String stringWeight = String.format("%.1f", numEdges - totWeight);
		System.out.print("W: " + stringWeight);
		System.out.println("\n\n" + "-".repeat(60) + "\n");
	}
}
import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashSet;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.Stack;

class Graph {

	Data data = null;
	boolean initialized = false;
	
	public void readData(File fileNodes, File fileEdges) {
		
		data = new Data(this);
		
		Scanner scannerNode = null;
		Scanner scannerEdge = null;

		try {
			scannerNode = new Scanner(fileNodes);
			scannerEdge = new Scanner(fileEdges);
		}

		catch (FileNotFoundException e) {
			if (scannerNode == null) {
				System.out.println("File '" + fileNodes + "' not found!");
			} else {
				System.out.println("File '" + fileEdges + "' not found!");
			}
			return;
		}

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
			String name = bits[1].strip().toLowerCase();

			Node temp = new Node(nmid, name);

			for (int i = 2; i < bits.length; i++) {

				if (data.edges.containsKey(bits[i])) {
					Edge tempEdge = data.edges.get(bits[i]);

					tempEdge.nodes.add(temp);
				}
			}

			data.addNode(nmid, temp);
		}

		scannerNode.close();
		scannerEdge.close();
	}

	public void createGraph() {
		
		if (data == null) {
			System.out.println("no data found!");
			return;
		}
		
		int index = 0;
		for (Edge e : data.edges.values()) {
			
			HashSet<Node> temp = new HashSet<>(e.nodes);
			
			while (temp.size() > 0) {
				
				Node n1 = temp.iterator().next();
				temp.remove(n1);
				
				for (Node n2 : temp) {
					n1.addRelation(n2, e);
					n2.addRelation(n1, e);
					index++;
				}
			}
		}

		System.out.println("Nodes: " + data.nodes.size());
		System.out.println("Edges: " + index);
		
		initialized = true;
	}
	
	public boolean isReady() {
		return initialized;
	}
	
	public String getActor(String name) {

		String nname = name.strip().toLowerCase();
		
		for (Node n : data.nodes.values()) {
			
			if (nname.equals(n.name)) {
				return n.nmid;
			}
		}

		return null;
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

		while (L0.size() > 0) {
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
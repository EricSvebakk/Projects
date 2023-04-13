import java.util.HashMap;
import java.util.HashSet;

//
public class Node implements Comparable<Node> {
	HashMap<Node, Edge> nodes = null;
	// HashSet<Edge> edges = null;
	String nmid;
	String name;
	double dValue = 0;

	public Node(String nmid, String name) {
		this.nmid = nmid;
		this.name = name;
		this.nodes = new HashMap<>();
		// this.edges = new HashSet<>();
	}

	public void addRelation(Node n2, Edge edge) {
		
		// nodes.put(edge, n2);
		
		// if (nodes.containsKey(edge)) {	
			
		// } else {
			
		// }
		
		if (nodes.containsKey(n2)) {
			
			if (edge.rating > nodes.get(n2).rating) {
				nodes.put(n2, edge);
				// edges.add(edge);
			}
		} else {
			nodes.put(n2, edge);
			// edges.add(edge);
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
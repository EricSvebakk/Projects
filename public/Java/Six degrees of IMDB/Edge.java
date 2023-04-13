import java.util.HashSet;

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
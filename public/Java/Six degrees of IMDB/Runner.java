// package Obliger.Oblig2;

import java.io.File;

public class Runner {

	public static void main(String[] args) {
		
		File actors = new File("data/actors.tsv");
		File movies = new File("data/movies.tsv");
		
		Graph graph = new Graph(actors, movies);
		
		System.out.println("\nOppgave 1\n");
		graph.createGraph();
		
		System.out.println("\nOppgave 2\n");
		graph.shortestPath("nm2255973", "nm0000460");
		graph.shortestPath("nm0424060", "nm0000243");
		graph.shortestPath("nm4689420", "nm0000365");
		graph.shortestPath("nm0000288", "nm0001401");
		graph.shortestPath("nm0031483", "nm0931324");
		
		System.out.println("\nOppgave 3\n");
		graph.chillestPath("nm2255973", "nm0000460");
		graph.chillestPath("nm0424060", "nm0000243");
		graph.chillestPath("nm4689420", "nm0000365");
		graph.chillestPath("nm0000288", "nm0001401");
		graph.chillestPath("nm0031483", "nm0931324");
		
		System.out.println("\nOppgave 4\n");
		graph.findComponents();
	}
	
	/*
	 * eventloop for Six Degrees program.
	 */
	public static void eventloop() {
		
	}
}
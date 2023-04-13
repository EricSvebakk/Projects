// package Obliger.Oblig2;

import java.io.File;
import java.util.Scanner;

public class Runner {

	static Graph graph;
	
	public static void main(String[] args) {
		
		File actors = new File("data/actors.tsv");
		File movies = new File("data/movies.tsv");
		
		graph = new Graph();
		
		System.out.println("reading data!\n");
		graph.readData(actors, movies);
		
		System.out.println("creating graph!\n");
		graph.createGraph();
		
		if (graph.isReady()) {
			eventloop();
		}
		else {
			System.out.println("graph is not initialized!");
		}
	}
	
	/*
	 * eventloop for Six Degrees program.
	 */
	public static void eventloop() {
		
		boolean loop = true;
		String cmd = "";
		Scanner input = new Scanner(System.in);
		
		while (loop) {
			
			System.out.println("\n" +
				"Available commands:\n" +
				"0. exit\n" +
				"1. find actor/actress\n" +
				"2. find shortest path\n" +
				"3. find chillest path\n" +
				"4. find components\n"
			);
			
			cmd = input.nextLine();
			
			if (cmd.equals("0")) {
				System.out.println("exiting!");
				loop = false;
			}
			
			else if (cmd.equals("1")) {
				System.out.print("actor: ");
				
				cmd = input.nextLine();
				cmd = graph.getActor(cmd);
				
				System.out.println(cmd);
			}
			
			else if (cmd.equals("2")) {
				System.out.print("actor #1: ");
				String a1 = graph.getActor(input.nextLine());
				
				System.out.print("actor #2: ");
				String a2 = graph.getActor(input.nextLine());
				
				graph.shortestPath(a1, a2);
			}
			
			else if (cmd.equals("3")) {
				System.out.print("actor #1: ");
				String a1 = graph.getActor(input.nextLine());

				System.out.print("actor #2: ");
				String a2 = graph.getActor(input.nextLine());

				graph.chillestPath(a1, a2);
			}
			
			else if (cmd.equals("4")) {
				// System.out.println("'c n: k' = there is  is a set c of k people who can reach n-1 other people.");
				graph.findComponents();
			}
			
			else {
				System.out.println("undefined command!");
			}
		}
		
		input.close();
		
	}
}
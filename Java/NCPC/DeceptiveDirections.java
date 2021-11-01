
// import java.io.BufferedReader;
// import java.io.IOException;
// import java.io.InputStreamReader;
// import java.io.PrintWriter;
// import java.util.HashMap;
// import java.util.HashSet;


// class DeceptiveDirections {
	
// 	public static void main(String[] args) {
		
// 		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
// 		// PrintWriter writer = new PrintWriter(System.out);
		
// 		String lim;
// 		try {
// 			lim = br.readLine();
// 		} catch (IOException e) {
// 			lim = "0";
// 		}
		
// 		String[] bits = lim.split(" ");
		
// 		int w = Integer.parseInt(bits[0]);
// 		int h = Integer.parseInt(bits[0]);
		
// 		String[][] maze = new String[w][h];
// 		HashSet<String> dirs = new HashSet<>();
// 		HashMap<Integer, String> world = new HashMap<>();
		
// 		String line;
// 		int index;
		
// 		dirs.add("N");
// 		dirs.add("S");
// 		dirs.add("E");
// 		dirs.add("W");
		
		
// 		for (int y = 0; y < maze.length; y++) {
			
// 			try {	
// 				line = br.readLine();
// 			} catch (IOException e) {
// 				return;
// 			}
			
// 			for (int x = 0; x < maze[y].length; x++) {
// 				maze[y][x] = line.substring(x, x+1);
				
// 				if (maze[y][x].equals("S")) {
// 					index = x + (y * w);
// 					world.put(index, "S");
// 				}
// 			}
// 		}
		
// 		System.out.println(world);
		
// 		String path;
// 		try {
// 			path = br.readLine();
// 		} catch (IOException e) {
// 			return;
// 		}
		
		
// 		String dir;
// 		int pos = 0;
// 		HashMap<Integer, String> worldTemp = new HashMap<>();
		
// 		while (pos < path.length()) {
			
// 			dir = path.substring(pos, pos + 1);
// 			dirs.remove(dir);
			
// 			for (int ind : world.keySet()) {
				
// 				for (String d : dirs) {
					
// 					if (maze[ind % h][ind / w].equals("#")) {
// 						switch(d) {
// 							case "N":
								
// 								worldTemp.put(ind - w, "X");
// 								break;
// 							case "S":
// 								worldTemp.put(ind + w, "X");
// 								break;
// 							case "W":
// 								worldTemp.put(ind - 1, "X");
// 								break;
// 							case "E":
// 								worldTemp.put(ind + 1, "X");
// 								break;
// 						}
// 					}
// 				}
// 			}
// 			world = new HashMap<>(worldTemp);
			
// 			dirs.add(dir);
// 			pos++;
// 		}
		
		
// 		System.out.println(world);
		
// 		for (int y = 0; y < maze.length; y++) {
// 			for (int x = 0; x < maze[y].length; x++) {
				
// 				index = x + (y * w);
				
// 				if (world.containsKey(index)) {
// 					maze[y][x] = "!";
// 				}
				
// 				System.out.print(maze[y][x] + " ");
// 			}
// 			System.out.println();
// 		}
			
// 	}
	
// }
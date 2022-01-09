package testing;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;

/**
 *  Contains methods for processing Relational Databases.
 */
public class RDB2 {
	
	HashMap<String, String> FDs;
	String attributes;
	private int longestFD = 0;
	
	
	public RDB2(File f) {
	
		Scanner s;
		try {
			s = new Scanner(f);
		}

		catch (FileNotFoundException e) {
			System.out.println("file '" + f + "' not found.");
			return;
		}
		
		this.attributes = s.nextLine();

		this.FDs = new HashMap<>();
		while (s.hasNextLine()) {
			String[] a = s.nextLine().split("->");

			this.FDs.put(a[0], a[1]);
			if (a[0].length() > longestFD) {
				longestFD = a[0].length();
			}
		}

		s.close();
	}
	
	public HashMap<String, String> getNF() {
		
		
		return null;
	}
	
	public String toString() {
		
		String line = "\n================================\n";

		String s = line;

		s += "\nR(" + attributes + ")\n\n";
		s += "FDs\n";

		for (String c : FDs.keySet()) {
			String pad = String.format("%" + (longestFD + 1 - c.length()) + "s", "");
			s += c + pad + "-> " + FDs.get(c) + "\n";
		}

		s += line;

		return s;
	}
}

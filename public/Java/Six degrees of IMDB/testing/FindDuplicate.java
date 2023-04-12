
// package Obliger.Oblig2;

// import java.io.File;
// import java.io.FileNotFoundException;
// import java.util.Scanner;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;


public class FindDuplicate {
	
	public static void input(ArrayList<String> raw) {
		
		// File file1 = new File(args[0]);
		// Scanner scanner;

		// try {
		// scanner = new Scanner(file1);
		// }
		// catch (FileNotFoundException e) {
		// System.out.println("Fil '"+ file1 + "' ikke funnet!");
		// return;
		// }

		// ArrayList<String> raw = new ArrayList<>();
		// while (scanner.hasNextLine()) {
		// raw.add(scanner.nextLine());
		// }

		HashSet<String> unique = new HashSet<>(raw);
		ArrayList<String> dupes = new ArrayList<>(raw);

		for (String s : unique) {
			dupes.remove(s);
		}

		HashMap<String, Integer> result = new HashMap<>();
		for (String s1 : unique) {

			int l = 0;
			for (String s2 : dupes) {

				if (s1.equals(s2)) {
					l++;
				}
			}
			if (l > 0) {
				result.put(s1, l);
			}
		}

		System.out.println("\n=======================");
		for (String dupe : result.keySet()) {
			System.out.println(result.get(dupe) + " " + " " + dupe);
		}
		System.out.println("=======================");
		System.out.println(raw.size() + " - " + unique.size() + " = " + (raw.size() - unique.size())+ "\n");

	}
}




import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Arrays;


/**
 * Contains methods for processing Relational Databases.
 */
class RDB {
	
	HashMap<String, String> RDB_FDs;
	HashMap<String, String> RDB_Closures;
	HashMap<String, String> RDB_NFs;
	HashSet<String> RDB_CKs;
	String RDB_CAs;
	String RDB_A;
	
	private int length = 0;
	String line = "\n================================\n";
	
	public RDB(File f) {
		
		Scanner s;
		try {s = new Scanner(f);}
		catch (FileNotFoundException e) {
			System.out.println("file '" + f + "' not found.");
			return;
		}

		this.RDB_A = s.nextLine();
		
		this.RDB_FDs = new HashMap<>();
		
		while (s.hasNextLine()) {
			String[] a = s.nextLine().split("->");

			RDB_FDs.put(a[0], a[1]);
			if (a[0].length() > length) {
				length = a[0].length();
			}
		}
		
		this.RDB_CAs = findCA(this.RDB_FDs);
		this.RDB_CKs = findCK(this.RDB_CAs, this.RDB_A, this.RDB_FDs);
		
		this.RDB_Closures = new HashMap<>();
		
		for (String FD : this.RDB_FDs.keySet()) {
			this.RDB_Closures.put(FD, getClosure(FD, RDB_FDs));
		}
		
		this.RDB_NFs = findNFs(RDB_FDs, RDB_CKs);
		
		s.close();
	}
	
	/**
	 * Finds all elements related to "keys" using recursion
	 * @param reqA : all attributes required to be in a combination
	 * @param avlA : all attributes available to be used to create a combination
	 * @param cLength : length of a single combination
	 */
	private HashSet<String> findCombos(String reqA, String avlA, int cLength) {
		return combosRecursion(reqA, avlA, cLength, new HashSet<>());
	}
	
	/**
	 * Internal method used by getClousure() for finding closure. Uses recursion.
	 * @param reqA : all attributes required to be in a combination
	 * @param avlA : all attributes available to be used to create a combination
	 * @param cLength : Length of a single combination
	 * @param combos : contains all combinations (return-value)
	 */
	private HashSet<String> combosRecursion(String reqA, String avlA, int cLength, HashSet<String> combos) {

		combos.add(reqA);

		if (reqA.length() < cLength) {
			
			for (char a : avlA.toCharArray()) {
				
				if (!reqA.contains(String.valueOf(a))) {					
					
					char[] letters_temp = (reqA + a).toCharArray();
					
					Arrays.sort(letters_temp);
					combos.add(String.valueOf(letters_temp));
					
					combos = combosRecursion(String.valueOf(letters_temp), avlA, cLength, combos);
				}
			}
		}

		return combos;
	}
	
	/**
	 * Creates closure for the given attributes
	 * @param A contains all attributes to include in closure
	 * @param FDs functional depedencies to use for finding closure
	 * @return A string containing all attributes related to the given attributes
	 */
	public String getClosure(String A, HashMap<String, String> FDs) {
		return closureRecursion(A, FDs, 0);
	}
	
	/**
	 * Internal method used by getClousure() for finding closure. Uses recursion.
	 * @param A contains all attributes to include in closure
	 * @param size of closure, used for recursion-condition
	 * @param FDs functional depedencies to use for finding closure
	 * @return A closure of all attributes related to attributes
	 */
	private String closureRecursion(String A, HashMap<String, String> FDs, int size) {
		
		String copyA = "" + A;
		
		for (char a : A.toCharArray()) {
			String attribute = String.valueOf(a);	
			
			if (FDs.containsKey(attribute) && !copyA.contains(FDs.get(attribute))) {
		
				for (char i : FDs.get(attribute).toCharArray()) {
					
					if (!copyA.contains(String.valueOf(i))) {
						copyA += String.valueOf(i);
					}
				}
			}
			
			HashSet<String> combos = findCombos("", copyA, length);
			
			for (String c : combos) {
				if (FDs.containsKey(c)) {
					
					for (char j : FDs.get(c).toCharArray()) {
						if (!copyA.contains(String.valueOf(j))) {
							
							copyA += String.valueOf(j);
						}
					}
				}
			}
			
			char[] temp = copyA.toCharArray();
			Arrays.sort(temp);
			copyA = String.valueOf(temp);
			
			if (copyA.length() != size) {
				copyA = closureRecursion(copyA, FDs, copyA.length());
			}
		}

		return copyA;
	}
	
	/**
	 * Returns a string containing candidate-keys for the relation
	 * @param FDs functional-dependencies for finding CA
	 */
	public String findCA(HashMap<String,String> FDs) {
		
		String CA = "";
		String left = "";
		String right = "";

		for (String a : FDs.keySet()) {

			for (char attribute : a.toCharArray()) {
				if (!left.contains(String.valueOf(attribute))) {
					left += attribute;
				}
			}

			for (char attribute : FDs.get(a).toCharArray()) {
				if (!right.contains(String.valueOf(attribute))) {
					right += attribute;
				}
			}
		}

		for (char attribute : left.toCharArray()) {
			if (!right.contains(String.valueOf(attribute))) {

				char[] temp = (CA + attribute).toCharArray();
				Arrays.sort(temp);
				CA = String.valueOf(temp);
			}
		}
		
		return CA;
	}
	
	/**
	 * Returns a string containing candidate-keys for the relation
	 * @param CA candidate-keys to include in each candidate-key
	 * @param A attributes to be considered for each candidate-key
	 * @param FDs determine valid attribute-combinations for a candidate-key
	 */
	public HashSet<String> findCK(String CA, String A, HashMap<String, String> FDs) {
		
		HashSet<String> candidateKeys = new HashSet<>();
		HashSet<String> combos = findCombos(CA, A, A.length());
		
		for (String attribute : combos) {

			String closure_temp = getClosure(attribute, FDs);
			
			if (closure_temp.length() == A.length()) {
				candidateKeys.add(attribute);
			}
		}
		
		HashSet<String> copy = new HashSet<>(candidateKeys);
		
		for (String a : candidateKeys) {
			
			HashSet<String> temp = new HashSet<>(candidateKeys);
			temp.remove(a);
			
			for (String b : temp) {
				
				String shortest = "";
				String longest = "";
				
				if (a.length() < b.length()) {
					shortest = a;
					longest = b;
				} else {
					shortest = b;
					longest = a;
				}
				
				int matches = 0;
				for (char ac : a.toCharArray()) {
					for (char bc : b.toCharArray()) {
						if (String.valueOf(ac).equals(String.valueOf(bc))) {
							matches++;
						}
					}
				}
				
				if (matches == shortest.length()) {
					copy.remove(longest);
				}
			}
		}
		
		return copy;
	}
	
	/**
	 * Returns functional-dependencies that are valid for the given closure
	 * @param
	 * @param
	 */
	private HashMap<String, String> filterFDs(String closure, HashMap<String,String> FDs) {
		
		HashMap<String, String> filter = new HashMap<>();
		
		for (String key : FDs.keySet()) {
			
			int matchesLeft = 0;
			int matchesRight = 0;
			
			for (char i : key.toCharArray()) {
				if (closure.contains(String.valueOf(i))) {
					matchesLeft++;
				}
			}
			
			for (char i : FDs.get(key).toCharArray()) {
				if (closure.contains(String.valueOf(i))) {
					matchesRight++;
				}
			}
			
			if (matchesLeft == key.length() && matchesRight == FDs.get(key).length()) {
				filter.put(key, FDs.get(key));
			}
		} 
		
		return filter;
	}
	
	/**
	 * Prints an explanation for the normalform of each functional-dependency
	 * @param
	 * @param
	 */
	public HashMap<String,String> findNFs(HashMap<String, String> FDs, HashSet<String> CKs) {
		
		HashMap<String,String> NFs = new HashMap<>();
		
		outer:
		for (String a1 : FDs.keySet()) {
			System.out.println();
			
			String FD = a1 + " -> " + FDs.get(a1);
			
			for (String a2 : CKs) {
				if (a1.contains(a2)) {
					NFs.put(a1, "BCNF");
					System.out.println(FD + " er i BCNF");
					continue outer;
				}
			}
			System.out.println(FD + " bryter med BCNF fordi " + a1 + " er ikke en supernøkkel");
			
			for (String a2 : CKs) { 
				if (a2.contains(FDs.get(a1))) {
					NFs.put(a1, "3NF");
					System.out.println(FD + " er i 3NF");
					continue outer;
				}
			}
			System.out.println(FD + " bryter med 3NF fordi " + FDs.get(a1) + " er ikke et nøkkelattributt");
			
			boolean flag = true;
			for (String a2 : CKs) {
				if (a2.contains(a1)) {
					System.out.println(FD + " bryter med 2NF fordi " + a1 + " er del av en kandidatnøkkel");
					flag = false;
				}
			}
			
			if (flag) {
				NFs.put(a1, "2NF");
				System.out.println(FD + " er i 2NF");
				continue outer;
			}
			
			NFs.put(a1, "1NF");
			System.out.println(FD + " er i 1NF");
		}
		
		System.out.println(line);
		
		return NFs;
	}
	
	/**
	 * internal methode used in decompose() to check if a functional-dependency is BCNF or not.
	 * @param
	 * @param
	 */
	private boolean isBCNF(String keyFD, HashSet<String> CKs) {
		
		for (String a2 : CKs) {
			if (keyFD.contains(a2)) {
				return true;
			}
		}
		
		return false;
	}
	
	/**
	 * Contains a temporary relation.
	 * Internal class used for decompose() / decompose_rec().
	 */
	private class decompRelation {
		HashSet<String> CK;
		String closure;
		String R;
		boolean valid = true;
		
		/**
		 * @param R name of relation
		 * @param closure all attributes in relation
		 * @param CK candidate-keys for the relation
		 */
		public decompRelation(String R, String closure, HashSet<String> CK) {
			this.R = R;
			this.closure = closure;
			this.CK = CK;
		}
		
		public String toString() {
			return R + "(" + closure + ") " + CK;
		}
	}
	
	/**
	 * Decomposes a relation to a set of BCNF relations.
	 * @param keyFD left-side of a functional-dependency
	 */
	public void decompose(String keyFD) {
		
		HashMap<String, decompRelation> decomps = new HashMap<>();
		
		String R = "R";
		decomps.put(R, new decompRelation(R, RDB_A, RDB_CKs));
		
		System.out.println(keyFD + " -> " + RDB_FDs.get(keyFD) + " (" + RDB_NFs.get(keyFD) + ")\n");
		System.out.println(decomps.get(R));
		
		if (!isBCNF(keyFD, RDB_CKs)) {
			System.out.print(keyFD + " -> " + RDB_FDs.get(keyFD) + " bryter med BCNF fordi ");
			System.out.println(keyFD + " er ikke en supernøkkel for " + R);
			
			decomps.get(R).valid = false;
			decomps = decompose_rec(keyFD, RDB_A, decomps, R, 0);
			
			System.out.println("\n");
			for (String dR : decomps.keySet()) {
				if (decomps.get(dR).valid) {
					System.out.println(decomps.get(dR));
				}
			}
		}
		
		System.out.println(line);
	}
	
	/**
	 * Decomposes a relation to a set of BCNF relations.
	 * @param keyFD left-side of a functional-dependency
	 * @param closure 
	 * @param data contains all recursively-created relations
	 * @param R relation-name for next recursion-step
	 * @param index recursive index for indenting console
	 */
	private HashMap<String, decompRelation> decompose_rec(String keyFD, String closure, HashMap<String, decompRelation> data, String R, int index) {
		
		String pad = String.format("%" + (4 + (4 * index++)) + "s", "");
		String R1 = R + "1";
		String R2 = R + "2";
		
		
		String R1Closure = getClosure(keyFD, RDB_FDs);
		HashMap<String, String> R1FDs = filterFDs(R1Closure, RDB_FDs);
		HashSet<String> R1CKs = findCK("", R1Closure, R1FDs);
		data.put(R1, new decompRelation(R1, R1Closure, R1CKs));
		
		
		String R2Closure = closure;
		for (char i : R1Closure.toCharArray()) {
			if (!keyFD.contains(String.valueOf(i))) {
				R2Closure = R2Closure.replace(String.valueOf(i), "");
			}
		}
		HashMap<String, String> R2FDs = filterFDs(R2Closure, RDB_FDs);
		HashSet<String> R2CKs = findCK("", R2Closure, R2FDs);
		data.put(R2, new decompRelation(R2, R2Closure, R2CKs));
		
		
		System.out.println("\n" + pad + keyFD + "+ = {" + R1Closure + "}");
		System.out.println("\n" + pad + data.get(R1));
		HashMap<String, String> filterR1 = filterFDs(data.get(R1).closure, RDB_FDs);
		
		for (String i : filterR1.keySet()) {
			if (isBCNF(i, data.get(R1).CK)) {
				// System.out.println(pad + i + " -> " + filterR1.get(i) + " gjelder og er gyldig for " + R1);
				System.out.println(pad + "Har " + i + " -> " + filterR1.get(i) + " som følger BCNF");
			}
		}
		
		for (String i : filterR1.keySet()) {
			if (!isBCNF(i, data.get(R1).CK)) {
				// System.out.print(pad + i + " -> " + RDB_FDs.get(i) + " gjelder og bryter med BCNF fordi ");
				System.out.print(pad + "Har " + i + " -> " + filterR1.get(i) + " som bryter BCNF fordi ");
				System.out.println(i + " er ikke en supernøkkel for " + R1);
				
				data.get(R1).valid = false;
				data = decompose_rec(i, data.get(R1).closure, data, R1, index);
				// break;
			}
		}
		
		System.out.println("\n" + pad + data.get(R2));
		HashMap<String, String> filterR2 = filterFDs(data.get(R2).closure, RDB_FDs);
		
		for (String i : filterR2.keySet()) {
			if (isBCNF(i, data.get(R2).CK)) {
				// System.out.println(pad + i + " -> " + filterR2.get(i) + " gjelder og er gyldig for " + R2);
				System.out.println(pad + "Har " + i + " -> " + filterR2.get(i) + " som følger BCNF");
			}
		}
		
		for (String i : filterR2.keySet()) {
			if (!isBCNF(i, data.get(R2).CK)) {
				// System.out.print(pad + i + " -> " + RDB_FDs.get(i) + " gjelder og bryter med BCNF fordi ");
				System.out.print(pad + "Har " + i + " -> " + filterR2.get(i) + " som bryter BCNF fordi ");
				System.out.println(i + " er ikke en supernøkkel for " + R2);
				
				data.get(R2).valid = false;
				data = decompose_rec(i, data.get(R2).closure, data, R2, index);
				// break;
			}
		}
		
		return data;
	}
	
	/**
	 * Shows information about the relation and related functional dependencies.
	 * Includes candidate-attributes, candidate-keys and closures for each
	 * attribute of the relation.
	 */
	public String toString() {
		
		String s = "";
		
		s += "\nR(" + RDB_A + ")\n\n";
		s += "FDs\n";
		
		for (String c : RDB_FDs.keySet()) {
			
			String i = RDB_NFs.get(c);
			
			String pad1 = String.format("%" + (length + 1 - c.length()) + "s", "");
			String pad2 = String.format("%" + (4 + 1 - i.length()) + "s", "");

			s += c + pad1 + "-> " + RDB_FDs.get(c) + pad2 + "(" + i + ")\n";
		}
		s += "\nCA\n";
		s += "[" + this.RDB_CAs + "]\n\n";
		s += "CK\n";
		s += this.RDB_CKs + "\n\n";
		
		for (String FD : RDB_Closures.keySet()) {
			String pad = String.format("%" + (length + 1 - FD.length()) + "s", "");
			s += FD + "+" + pad + " = " + this.RDB_Closures.get(FD) + "\n";
		}
		
		s += line;
		
		return s;
	}
}



import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Set;
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
	
	HashMap<String, Integer> NFs;
	
	private int length = 0;
	String line = "\n================================\n";
	
	public RDB(File f) {
		
		Scanner s;
		try {s = new Scanner(f);}
		catch (FileNotFoundException e) {
			System.out.println("file '" + f + "' not found.");
			return;
		}

		this.NFs = new HashMap<>();
		this.NFs.put("BCNF", 4);
		this.NFs.put("3NF", 3);
		this.NFs.put("2NF", 2);
		this.NFs.put("1NF", 1);
		
		this.RDB_A = s.nextLine();
		
		this.RDB_FDs = new HashMap<>();
		
		while (s.hasNextLine()) {
			String[] FD_temp = s.nextLine().split("->");

			char[] temp = FD_temp[0].toCharArray();
			Arrays.sort(temp);
			String determinant = String.valueOf(temp);
			
			temp = FD_temp[1].toCharArray();
			Arrays.sort(temp);
			String dependent = String.valueOf(temp);
			
			RDB_FDs.put(determinant, dependent);
			if (determinant.length() > length) {
				length = determinant.length();
			}
		}
		
		this.RDB_CAs = findCA(this.RDB_FDs, this.RDB_A);
		this.RDB_CKs = findCK(this.RDB_CAs, this.RDB_A, this.RDB_FDs);
		
		this.RDB_Closures = new HashMap<>();
		
		for (String FD : this.RDB_FDs.keySet()) {
			this.RDB_Closures.put(FD, getClosure(FD, RDB_FDs));
		}
		
		this.RDB_NFs = findNFs(RDB_FDs, RDB_CKs);
		
		s.close();
	}
	
	/**
	 * Finds all combinations of n elements (where n goes from 0 to k)
	 * @param requiredAttributes : attributes required to be in a combination
	 * @param availableAttributes : attributes available for creating a combination
	 * @param k : maximum length of a single combination
	 */
	private HashSet<String> findUpToKCombinations(String requiredAttributes, String availableAttributes, int k) {
		
		if (requiredAttributes.length() > k) {
			return null;
		}
		
		return combosRecursion(requiredAttributes, availableAttributes, k, new HashSet<>());
	}
	
	/**
	 * Internal method used by findUpToKCombinations() for finding [up-to-k]-combinations. Uses recursion.
	 * @param reqAttrs : required attributes to be in a combination
	 * @param avlAttrs : available attributes for creating a combination
	 * @param cLength : Length of a single combination
	 * @param result : recursive return-value containing all combinations
	 */
	private HashSet<String> combosRecursion(String reqAttrs, String avlAttrs, int cLength, HashSet<String> result) {
		
		char[] temp = String.join("", reqAttrs).toCharArray();
		Arrays.sort(temp);	
		String reqAttrsSorted = String.valueOf(temp);
		
		result.add(reqAttrsSorted);
		
		// Iterate over attributes and create [up-to-k]-combinations via recursive branches
		for (char attr : avlAttrs.toCharArray()) {
			
			String newReqAttrs = reqAttrsSorted+attr;
			String newAvlAttrs = avlAttrs.replace(String.valueOf(attr), "");
			
			// Only recur if newReqA is shorter than cLength
			// This limits the results to only containing [up-to-k]-combinations
			if (newReqAttrs.length() <= cLength) {
				result = combosRecursion(newReqAttrs, newAvlAttrs, cLength, result);
			}
		}
		
		return result;
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
	 * @param FDs functional depedencies to use for finding closure
	 * @param size of closure, used for recursion-condition
	 * @return A closure of all attributes related to attributes
	 */
	private String closureRecursion(String A, HashMap<String, String> FDs, int size) {
		
		// result
		HashSet<String> closure = new HashSet<>(Arrays.asList(A.split("")));
		
		// combinations made from the closure-attributes 
		HashSet<String> determinantCombos = findUpToKCombinations("", String.join("", closure), length);
		
		// Iterate possible combinations
		for (String dc : determinantCombos) {
			
			// check if dc is a valid determinant 
			if (FDs.containsKey(dc)) {
				String dependent = FDs.get(dc);
				
				for (char attribute : dependent.toCharArray()) {
					closure.add(String.valueOf(attribute));
				}
				
				// recur if new attributes were added from dc
				if (closure.size() != size) {
					// System.out.println("NEW  : " + closure);
					return closureRecursion(String.join("", closure), FDs, closure.size());
				}
			}
		}
		
		return String.join("", closure);
	}
	
	/**
	 * Returns a string containing candidate-attributes for the relation
	 * @param FDs functional-dependencies for finding CA
	 * @param allAttributes to check for attributes not in any FD
	 */
	public String findCA(HashMap<String,String> FDs, String allAttibutes) {
		
		String CA = "";
		String left = "";
		String right = "";

		for (String FD : FDs.keySet()) {

			for (char attribute : FD.toCharArray()) {
				if (!left.contains(String.valueOf(attribute))) {
					left += attribute;
				}
			}

			for (char attribute : FDs.get(FD).toCharArray()) {
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
		
		last:
		for (char attribute : allAttibutes.toCharArray()) {
			
			if (left.contains(String.valueOf(attribute))) continue last;
			if (right.contains(String.valueOf(attribute))) continue last;
			
			char[] temp = (CA + attribute).toCharArray();
			Arrays.sort(temp);
			CA = String.valueOf(temp);
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
		HashSet<String> combos = findUpToKCombinations(CA, A, A.length());
		
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
	 * Prints an explanation for the normalform of each functional-dependency
	 * @param FDs which functional-dependencies to check
	 * @param CKs which candidate-keys to base the normalform on
	 */
	public HashMap<String, String> findNFs(HashMap<String, String> FDs, HashSet<String> CKs) {

		HashMap<String, String> NFs = new HashMap<>();

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
	 * Returns functional-dependencies that are valid for the given closure
	 * @param closure the attributes used for filtering FDs
	 * @param FDs all FDs to
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
		
		String validFD = keyFD;
		if (!RDB_FDs.containsKey(validFD)) {
			
			System.out.println(validFD + " is not an FD!");
			
			int bestInt = 0;
			String bestFD = "";
			
			for (String FD : RDB_NFs.keySet()) {
				
				String NF = RDB_NFs.get(FD);
				int temp = NFs.get(NF);
				
				if (!NF.equals("BCNF") && temp >= bestInt && FD.length() > bestFD.length()) {
					bestInt = temp;
					bestFD = FD;
				}
			}
			
			validFD = bestFD;
			System.out.println(validFD);
			
			if (!RDB_FDs.containsKey(validFD)) {
				System.out.println("non-BCNF FD not found!");
				return;
			}
			
		}
		else {
			System.out.println("FD '" + keyFD + "' found!");
		}
		
		HashMap<String, decompRelation> decomps = new HashMap<>();
		
		String R = "R";
		decomps.put(R, new decompRelation(R, RDB_A, RDB_CKs));
		
		System.out.println(validFD + " -> " + RDB_FDs.get(validFD) + " (" + RDB_NFs.get(validFD) + ")\n");
		System.out.println(decomps.get(R));
		
		if (!isBCNF(validFD, RDB_CKs)) {
			System.out.println(validFD + " -> " + RDB_FDs.get(validFD) + " bryter med BCNF fordi " + validFD + " er ikke en supernøkkel for " + R);
			
			decomps.get(R).valid = false;
			decomps = decompose_rec(validFD, RDB_A, decomps, R, 0);
			
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
	 * Breaks down R(X) to R1(Y+) and R2(X-Y+) using FD F->Y
	 * @param keyFD left-side of a functional-dependency
	 * @param closure all relevant attributes for keyFD
	 * @param data contains all recursively-created relations
	 * @param R relation-name for next recursion-step
	 * @param index recursive index for indenting console
	 */
	private HashMap<String, decompRelation> decompose_rec(String keyFD, String closure, HashMap<String, decompRelation> data, String R, int index) {
		
		String pad = String.format("%" + (4 + (4 * index++)) + "s", "");
		String R1 = R + "1";
		String R2 = R + "2";
		
		// Breaks down R(X) to R1(Y+)
		String R1Closure = getClosure(keyFD, RDB_FDs);
		HashMap<String, String> R1FDs = filterFDs(R1Closure, RDB_FDs);
		HashSet<String> R1CKs = findCK("", R1Closure, R1FDs);
		data.put(R1, new decompRelation(R1, R1Closure, R1CKs));
		
		// Breaks down R(X) to R2(X-Y+)
		String R2Closure = closure;
		for (char i : R1Closure.toCharArray()) {
			if (!keyFD.contains(String.valueOf(i))) {
				R2Closure = R2Closure.replace(String.valueOf(i), "");
			}
		}
		HashMap<String, String> R2FDs = filterFDs(R2Closure, RDB_FDs);
		HashSet<String> R2CKs = findCK("", R2Closure, R2FDs);
		data.put(R2, new decompRelation(R2, R2Closure, R2CKs));
		
		// Closure of current FD
		System.out.println("\n" + pad + keyFD + "+ = {" + R1Closure + "}");
		
		// R1 and relevant FD's for R1
		System.out.println("\n" + pad + data.get(R1));
		HashMap<String, String> filterR1 = filterFDs(data.get(R1).closure, RDB_FDs);
		
		// Lists all valid BCNF FD's for R1
		for (String i : filterR1.keySet()) {
			if (isBCNF(i, data.get(R1).CK)) {
				System.out.println(pad + "Har " + i + " -> " + filterR1.get(i) + " som følger BCNF");
			}
		}
		
		// Recursively calls decompose_rec() on a valid non-BCNF FD for R1
		for (String i : filterR1.keySet()) {
			if (!isBCNF(i, data.get(R1).CK)) {
				System.out.print(pad + "Har " + i + " -> " + filterR1.get(i) + " som bryter BCNF fordi " + i + " er ikke en supernøkkel for " + R1);
				
				data.get(R1).valid = false;
				data = decompose_rec(i, data.get(R1).closure, data, R1, index);
				break;
			}
		}
		
		// R2 and relevant FD's for R2
		System.out.println("\n" + pad + data.get(R2));
		HashMap<String, String> filterR2 = filterFDs(data.get(R2).closure, RDB_FDs);
		
		// Lists all valid BCNF FD's for R2
		for (String i : filterR2.keySet()) {
			if (isBCNF(i, data.get(R2).CK)) {
				System.out.println(pad + "Har " + i + " -> " + filterR2.get(i) + " som følger BCNF");
			}
		}
		
		// Recursively calls decompose_rec() on a valid non-BCNF FD for R2
		for (String i : filterR2.keySet()) {
			if (!isBCNF(i, data.get(R2).CK)) {
				System.out.print(pad + "Har " + i + " -> " + filterR2.get(i) + " som bryter BCNF fordi " + i + " er ikke en supernøkkel for " + R2);
				
				data.get(R2).valid = false;
				data = decompose_rec(i, data.get(R2).closure, data, R2, index);
				break;
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
		
		s += "R(" + RDB_A + ")\n\n";
		s += "Functional dependencies\n";
		
		for (String c : RDB_FDs.keySet()) {
			
			String i = RDB_NFs.get(c);
			String pad1 = String.format("%" + (length + 1 - c.length()) + "s", "");
			String pad2 = String.format("%" + (4 + 1 - i.length()) + "s", "");
			
			s += c + pad1 + "-> " + RDB_FDs.get(c) + pad2 + "(" + i + ")\n";
		}
		
		s += "\nCandidate attributes\n[" + this.RDB_CAs + "]\n";
		s += "\nCandidate keys\n" + this.RDB_CKs + "\n";
		
		s += "\nFD closures\n";
		for (String FD : RDB_Closures.keySet()) {
			
			String pad = String.format("%" + (length + 1 - FD.length()) + "s", "");
			
			s += FD + "+" + pad + " = " + this.RDB_Closures.get(FD) + "\n";
		}
		
		s += "\nAttribute closures\n";
		for (char c : RDB_A.toCharArray()) {
			s += c + "+ = " + getClosure(String.valueOf(c), RDB_FDs) + "\n";
		}
		
		s += line;
		
		return s;
	}
}
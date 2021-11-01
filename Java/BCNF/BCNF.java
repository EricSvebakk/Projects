

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Arrays;

// import java.lang.Character.Subset;
// import java.time.temporal.Temporal;
// import java.util.ArrayList;
// import javax.crypto.Cipher;
// import javax.print.attribute.standard.Sides;


public class BCNF {
	
	public static void main(String[] args) {
		
		Scanner s1;
		Scanner s2;;
		
		try {
			s1 = new Scanner(new File("input1.txt"));
			s2 = new Scanner(new File("input3.txt"));
		}
		
		catch(FileNotFoundException e) {
			System.out.println("FILE FAILURE!");
			return;
		}
		
		Relation relation1 = new Relation(s1.nextLine());
		Relation relation2 = new Relation(s2.nextLine());
		
		
		while (s1.hasNextLine()) {
			relation1.addFD(s1.nextLine());
		}
		
		while (s2.hasNextLine()) {
			relation2.addFD(s2.nextLine());
		}
		
		
		System.out.println(relation1);
		System.out.println(relation2);
	}
}


class Relation {
	
	String allAttributes;
	HashMap<String, String> allFDs;
	
	int recI = 0;
	int length = 0;
	
	public Relation(String r) {
		
		// ADD FILE READING HERE
		
		this.allAttributes = r;
		this.allFDs = new HashMap<>();
	}
	
	
	public void addFD(String text) {
		String[] a = text.split("->");
		
		allFDs.put(a[0], a[1]);
		if (a[0].length() > length) {
			length = a[0].length();
		}
	}
	
	
	/**
	 * Finds all elements related to "keys" using recursion
	 * @param keys : a string containing all elements to include in closure
	 * @param closure : an empty hashset
	 */
	public HashSet<String> findCombos(String initAttrs, String attributes, int keyLength) {
		HashSet<String> combos = new HashSet<>();
		return combosRecursion(initAttrs, attributes, keyLength, combos);
	}
	
	
	/**
	 * Internal method used by getClousure() for finding closure. Uses recursion.
	 * @param initAttrs : all attributes required to be in a combination
	 * @param attributes : all attributes to be used to create a combination
	 * @param keyLength : Length of a single combination
	 * @param combos : contains all combinations (return-value)
	 */
	private HashSet<String> combosRecursion(String initAttrs, String attributes, int keyLength, HashSet<String> combos) {

		combos.add(initAttrs);

		if (initAttrs.length() < keyLength) {
			for (char a : attributes.toCharArray()) {
				if (!initAttrs.contains(String.valueOf(a))) {					
					
					
					char[] letters_temp = (initAttrs + a).toCharArray();
					
					Arrays.sort(letters_temp);
					combos.add(String.valueOf(letters_temp));
					
					combos = combosRecursion(String.valueOf(letters_temp), attributes, keyLength, combos);
				}
			}
		}

		return combos;
	}
	
	
	/**
	 * Finds all elements related to attributes
	 * @param attributes contains all elements to include in closure
	 * @return A closure of all elements related to input attributes
	 */
	public String getClosure(String attributes) {
		return closureRecursion(attributes, 0);
	}
	
	
	/**
	 * Internal method used by getClousure() for finding closure. Uses recursion.
	 * @param attributes contains all elements to include in closure
	 * @param size of closure, used for recursion-condition
	 * @return A closure of all elements related to attributes
	 */
	private String closureRecursion(String attributes, int size) {
		
		HashSet<String> combos = new HashSet<>();
		String newAttributes = "" + attributes;
		
		
		for (char attr : attributes.toCharArray()) {
			
			String attribute = String.valueOf(attr);	
			
			if (allFDs.containsKey(attribute) && !newAttributes.contains(allFDs.get(attribute))) {
				
				for (char i : allFDs.get(attribute).toCharArray()) {
					
					if (!newAttributes.contains(String.valueOf(i))) {
						newAttributes += String.valueOf(i);
					}
				}
			}
			
			combos = findCombos("", newAttributes, length);
			
			for (String i : combos) {
				if (allFDs.containsKey(i)) {
					
					for (char j : allFDs.get(i).toCharArray()) {
						if (!newAttributes.contains(String.valueOf(j))) {
							
							newAttributes += String.valueOf(j);
						}
					}
				}
			}
			
			char[] temp = newAttributes.toCharArray();
			Arrays.sort(temp);
			newAttributes = String.valueOf(temp);
			
			if (newAttributes.length() != size) {
				newAttributes = closureRecursion(newAttributes, newAttributes.length());
			}
		}

		return newAttributes;
	}
	
	
	public String findCandidateAttributes(HashMap<String,String> FDs) {
		
		String candidateAttributes = "";
		String left = "";
		String right = "";

		for (String attr : FDs.keySet()) {

			for (char i : attr.toCharArray()) {
				if (!left.contains(String.valueOf(i))) {
					left += i;
				}
			}

			for (char i : FDs.get(attr).toCharArray()) {
				if (!right.contains(String.valueOf(i))) {
					right += i;
				}
			}
		}

		for (char attr : left.toCharArray()) {
			if (!right.contains(String.valueOf(attr))) {

				char[] temp = (candidateAttributes + attr).toCharArray();
				Arrays.sort(temp);
				candidateAttributes = String.valueOf(temp);
			}
		}
		
		return candidateAttributes;
	}
	
	
	/**
	 * Finds all candidate-keys up to a certain length, using createCombo()
	 * @param keyLength limitation for key length
	 */
	public HashSet<String> findCandidateKeys(String candidateAttributes, String attributes) {
		
		
		HashSet<String> candidateKeys = new HashSet<>();
		
		HashSet<String> combos = findCombos(candidateAttributes, attributes, attributes.length());
		
		
		for (String attr : combos) {

			String closure_temp = getClosure(attr);
						
			
			if (closure_temp.length() == attributes.length()) {
				
				
				// System.out.println(closure_temp + " " + attr);
				
				combos = findCombos("", attr, attributes.length());
				
				
				// boolean flag = true;
				// for (String combo : combos) {
					
				// 	char[] a = combo.toCharArray();
					
					
				// 	for (char key : candidateAttributes.toCharArray()) {
						
				// 		char[] b = key.toCharArray();
						
				// 		Arrays.sort(a);
				// 		Arrays.sort(b);
						
				// 		if (Arrays.equals(a, b)) {
				// 			flag = false;
				// 		}
						
				// 	}
				// }
				
				
				// if (flag) {

				// 	char[] key = keys.toCharArray();
				// 	Arrays.sort(key);
					
				// }
				
				candidateKeys.add(attr);
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
				// System.out.print(a + " " + b + "|" + shortest);
				
				int matches = 0;
				for (char ac : a.toCharArray()) {
					for (char bc : b.toCharArray()) {
						
						if (String.valueOf(ac).equals(String.valueOf(bc))) {
							matches++;
						}
					}
				}
				
				if (matches == shortest.length()) {
				// System.out.println("|| " + longest);
					copy.remove(longest);
				}
			}
		}
		
		return copy;
	}
	
	
	/**
	 * Returns functional-dependencies that are valid for the given closure
	 * @param closure
	 * @return
	 */
	public HashMap<String, String> filterFDs(String closure, HashMap<String,String> FDs) {
		
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
	
	
	public HashSet<String> findBCNF(HashSet<String> candidateKeys, HashMap<String,String> FDs) {
		
		HashSet<String> BCNF = new HashSet<>();
		
		for (String attr : FDs.keySet()) {
			for (String key : candidateKeys) {
				
				int matches = 0;
				for (char i : key.toCharArray()) {
					if (attr.contains(String.valueOf(i))) {
						matches++;
					}
				}
				
				if (matches == key.length()) {
					BCNF.add(attr);
					// System.out.println("BCNF: YES | " + attr);
				}
			}
		}
		
		HashSet<String> copy = new HashSet<>(FDs.keySet());
		copy.removeAll(BCNF);
		
		
		// System.out.println(copy);
		
		String longest = "";
		for (String FD : copy) {
			
			String temp = getClosure(FD);
			
			if (temp.length() > longest.length()) {
				longest = temp;
			}
		}
		
		HashMap<String,String> temp = filterFDs(longest, FDs);
		
		// System.out.println("FILTER: " + temp);
		
		
		return BCNF;
	}
	
	
	/**
	 * Shows information about the relation and related functional dependencies.
	 * Includes candidate-attributes, candidate-keys and closures for each
	 * attribute of the relation.
	 */
	public String toString() {
		
		String line = "\n================================\n";
		
		String s = line;
		
		
		s += "\nR(" + allAttributes + ")\n\n";
		
		s += "FDs\n";
		for (String c : allFDs.keySet()) {
			String pad = String.format("%" + (length + 1 - c.length()) + "s", "");

			s += c + pad + "-> " + allFDs.get(c) + "\n";
		}
		
		
		String CA = findCandidateAttributes(allFDs);		
		s += "\nCA\n";
		s += "[" + CA + "]\n\n";
		
		
		HashSet<String> CK = findCandidateKeys(CA, allAttributes);
		s += "CK\n";
		s += CK + "\n\n";
		
		
		// HashMap<String,String> filter = filterFDs("ABF", allFDs);
		// System.out.println("filter: " + filter);
		
		s += "FDs in BCNF\n";
		s += findBCNF(CK, allFDs) + "\n\n";
		
		
		for (String FD : allFDs.keySet()) {
			
			String closure = getClosure(FD);
			String pad = String.format("%" + (length + 1 - FD.length()) + "s", "");
			
			s +=  FD + "+" + pad + " = " + closure + "\n";
		}
		
		s += line;
		
		return s;
	}
}
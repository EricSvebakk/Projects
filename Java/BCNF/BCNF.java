

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import javax.naming.spi.DirStateFactory.Result;

import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayList;
import java.util.Arrays;

// import java.lang.Character.Subset;
// import java.time.temporal.Temporal;
// import java.util.ArrayList;
// import javax.crypto.Cipher;
// import javax.print.attribute.standard.Sides;


public class BCNF {
	
	public static void main(String[] args) {
		
		Scanner s1;
		
		try {
			s1 = new Scanner(new File("input1.txt"));
		}
		
		catch(FileNotFoundException e) {
			System.out.println("FILE FAILURE!");
			return;
		}
		
		Relation relation1 = new Relation(s1.nextLine());
		
		while (s1.hasNextLine()) {
			relation1.addFD(s1.nextLine());
		}
		
		System.out.println(relation1);
		System.out.println(relation1.getBCNF("CDE") + "\n");
	}
}


class Relation {
	
	String allAttributes;
	HashMap<String, String> allFDs;
	String allCAs;
	HashSet<String> allCKs;
	
	
	int recI = 0;
	int length = 0;
	
	public Relation(String r) {
		
		// ADD FILE READING HERE
		
		this.allAttributes = r;
		this.allFDs = new HashMap<>();
		
		this.allCAs = findCandidateAttributes(this.allFDs);
		this.allCKs = findCandidateKeys(this.allCAs, this.allAttributes, this.allFDs);
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
	public String getClosure(String attributes, HashMap<String, String> FDs) {
		return closureRecursion(attributes, FDs, 0);
	}
	
	
	/**
	 * Internal method used by getClousure() for finding closure. Uses recursion.
	 * @param attributes contains all elements to include in closure
	 * @param size of closure, used for recursion-condition
	 * @return A closure of all elements related to attributes
	 */
	private String closureRecursion(String attributes, HashMap<String, String> FDs, int size) {
		
		HashSet<String> combos = new HashSet<>();
		String newAttributes = "" + attributes;
		
		
		for (char attr : attributes.toCharArray()) {
			
			String attribute = String.valueOf(attr);	
			
			if (FDs.containsKey(attribute) && !newAttributes.contains(FDs.get(attribute))) {
				
				for (char i : FDs.get(attribute).toCharArray()) {
					
					if (!newAttributes.contains(String.valueOf(i))) {
						newAttributes += String.valueOf(i);
					}
				}
			}
			
			combos = findCombos("", newAttributes, length);
			
			for (String i : combos) {
				if (FDs.containsKey(i)) {
					
					for (char j : FDs.get(i).toCharArray()) {
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
				newAttributes = closureRecursion(newAttributes, FDs, newAttributes.length());
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
	public HashSet<String> findCandidateKeys(String candidateAttributes, String attributes, HashMap<String, String> FDs) {
		

		HashSet<String> candidateKeys = new HashSet<>();
		
		HashSet<String> combos = findCombos(candidateAttributes, attributes, attributes.length());
		
		for (String attr : combos) {

			String closure_temp = getClosure(attr, FDs);
			
			if (closure_temp.length() == attributes.length()) {
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
				// System.out.println("YES");
			}
			else {
				// System.out.println(key + " " + key.length() + " " + matchesLeft);
				// System.out.println(FDs.get(key) + " " + FDs.get(key).length() + " " + matchesRight);
				// System.out.println();
			}
		} 
		
		return filter;
	}
	
	
	public boolean isBCNF(String keyFD, HashSet<String> CKs) {
		
		for (String ckey : CKs) {
			
			int matches = 0;
			for (char i : ckey.toCharArray()) {
				if (keyFD.contains(String.valueOf(i))) {
					matches++;
				}
			}
			
			if (matches == ckey.length()) {
				// System.out.println("YES\n");
				return true;
			}
		}
		
		// System.out.println("NO\n");
		
		return false;
	}
	
	class Data {
		private String R = "";
		private String closure = "";
		private HashSet<String> CK = new HashSet<>();
		private boolean valid = true;
		
		public void setVariables(String R, String closure, HashSet<String> CK) {
			this.R = R;
			this.closure = closure;
			this.CK = CK;
		}
		
		public void setNotValid() {
			valid = false;
		}
		
		public boolean getValidity() {
			return valid;
		}
		
		public String toString() {
			return R + "(" + closure + ")";
		}
	}
	
	public HashSet<Data> getBCNF(String keyFD) {
		
		String R = "R";
		
		HashMap<String, Data> data = new HashMap<>();
		
		data.put(R, new Data());
		data.get(R).setVariables(R, allAttributes, allCKs);
		
		if (!isBCNF(keyFD, allCKs)) {
			data.get(R).setNotValid();
			System.out.println(data.get(R) + " " + data.get(R).CK);
			data = BCNF_rec(keyFD, allAttributes, data, R, 0);
		}
		
		System.out.println();
		
		HashSet<Data> result = new HashSet<>();
		for (String i : data.keySet()) {
			if (data.get(i).valid) {
				result.add(data.get(i));
			}
		}
		
		return result;
	}
	
	private HashMap<String, Data> BCNF_rec(String notBCNF, String closure, HashMap<String, Data> data, String R, int index) {
		
		
		String R1 = R + "1";
		String R2 = R + "2";
		
		data.put(R1, new Data());
		String R1Closure = getClosure(notBCNF, allFDs);
		HashMap<String, String> filtertemp = filterFDs(R1Closure, allFDs);
		
		data.get(R1).setVariables(
			R1,
			R1Closure,
			findCandidateKeys("", R1Closure, filtertemp)
		);
		
		// System.out.println(data.get(R1) + " " + data.get(R1).CK);
		
		// findCandidateKeys(notBCNF, closure, allFDs);
		
		data.put(R2, new Data());
		data.get(R2).setVariables(
			R2,
			closure,
			data.get(R).CK
		);
			
		for (char i : data.get(R1).closure.toCharArray()) {
			if (data.get(R2).closure.contains(String.valueOf(i)) && !notBCNF.contains(String.valueOf(i))) {
				data.get(R2).closure = data.get(R2).closure.replace(String.valueOf(i), "");
			}
		}
		
		// String R2Closure = getClosure(notBCNF, allFDs);
		HashMap<String, String> filtertemp2 = filterFDs(data.get(R2).closure, allFDs);
		
		// data.get(R2).closure = R2Closure;
		data.get(R2).CK = findCandidateKeys("", data.get(R2).closure, filtertemp2);
		
		// System.out.println(data.get(R2) + " " + data.get(R2).CK);
		
		// if (true) {
		// 	return null;
		// }
		
		String pad = String.format("%" + (1 + (8 * index++)) + "s", "");
		System.out.println();
		System.out.println(pad + notBCNF + "+ = {" + closure + "}");
		System.out.println(pad + data.get(R1) + " " + data.get(R1).CK);
		System.out.println(pad + data.get(R2) + " " + data.get(R2).CK);
		System.out.println();
		
		
		// HashSet<String> R1FD = new HashSet<>();
		// R1FD.add(notBCNF);
		
		// HashSet<String> R2FD = new HashSet<>();
		// R2FD.add(data.get(R).CK);
		
		HashMap<String, String> filter;
		filter = filterFDs(data.get(R1).closure, allFDs);
		
		// System.out.println(R1FD + " " + R2FD);
		
		for (String i : filter.keySet()) {
			if (isBCNF(i, data.get(R1).CK)) {
				System.out.println(pad + i + " → " + filter.get(i) + " gjelder og er gyldig for " + R1);
			}
		}
		
		for (String i : filter.keySet()) {
			if (!isBCNF(i, data.get(R1).CK)) {
				System.out.print(pad + i + " → " + allFDs.get(i) + " gjelder og bryter med BCNF fordi ");
				System.out.println(i + " er ikke en supernøkkel for " + R1);
				
				data.get(R1).setNotValid();
				data = BCNF_rec(i, data.get(R1).closure, data, R1, index);
				break;
			}
		}
		
		filter = filterFDs(data.get(R2).closure, allFDs);
		
		for (String i : filter.keySet()) {
			if (isBCNF(i, data.get(R2).CK)) {
				System.out.println(pad + i + " → " + filter.get(i) + " gjelder og er gyldig for " + R2);
			}
		}
		
		for (String i : filter.keySet()) {
			if (!isBCNF(i, data.get(R2).CK)) {
				System.out.print(pad + i + " → " + allFDs.get(i) + " gjelder og bryter med BCNF fordi ");
				System.out.println(i + " er ikke en supernøkkel for " + R2);
				
				data.get(R2).setNotValid();
				data = BCNF_rec(i, data.get(R2).closure, data, R2, index);
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
		
		String line = "\n================================\n";
		
		String s = line;
		
		
		s += "\nR(" + allAttributes + ")\n\n";
		
		s += "FDs\n";
		for (String c : allFDs.keySet()) {
			String pad = String.format("%" + (length + 1 - c.length()) + "s", "");

			s += c + pad + "-> " + allFDs.get(c) + "\n";
		}
		
		
		s += "\nCA\n";
		s += "[" + this.allCAs + "]\n\n";
		
		
		s += "CK\n";
		s += this.allCKs + "\n\n";
		
		
		s += "FDs in BCNF\n";
		for (String key : allFDs.keySet()) {
			if (isBCNF(key, this.allCKs)) {
				s += "- " + key + "\n";
			}
		}
		s += "\n";
		
		for (String FD : allFDs.keySet()) {			
			String closure = getClosure(FD, allFDs);
			String pad = String.format("%" + (length + 1 - FD.length()) + "s", "");
			s +=  FD + "+" + pad + " = " + closure + "\n";
		}
		
		s += line;
		
		return s;
	}
}
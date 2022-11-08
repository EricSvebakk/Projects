// import java.security.KeyStore.Entry;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;
import java.util.Map.Entry;

public class SATSolver {
	
	public static void main(String[] args) {
		
		// satisfiable
		Formula f1 = new Formula("{{-p, r, -s}, {p, q, r, -s}, {-p, -t}, {-r}, {p, s}, {p, r, t}, {s, t}}");
		
		// satisfiable
		Formula f2 = new Formula("{{p, -q}, {-p, q}, {q, -r}, {s}, {-s, -q, -r}, {s, r}}");
		
		// unsatisfiable
		Formula f3 = new Formula("{{p, q, s, t}, {p, s, -t}, {q,-s, t}, {p,-s,-t}, {p,-q}, {-p}, {r}}");
		
		// unsatisfiable
		Formula f4 = new Formula("{{p, q, r},{p, q, -r},{p, -q, r},{p, -q, -r},{-p, q, r},{-p, q, -r},{-p, -q, r},{-p, -q, -r}}");
		
		// satisfiable
		Formula f5 = new Formula("{{p, q, r},{p, q, -r},{p, -q, r},{p, -q, -r},{-p, q, r},{-p, q, -r},{-p, -q, r}}");
		
		
		DPLL dpll = new DPLL();
		
		final double T1 = System.currentTimeMillis();
		String result = dpll.prove(f1, 1);
		final double T2 = System.currentTimeMillis();
		
		System.out.println(result);
		System.out.println("time: " + (T2 - T1) / 1000 + "s");
	}
	
}

class Formula {
	
	ArrayList<HashSet<String>> clauses;
	HashMap<String, Integer> literalValues;
	HashMap<String, Integer> literalOccurences;
	HashSet<HashSet<String>> clausesPropagated;
	
	/**
	 * Clause-form propopsitional formula
	 * @param input a string containing a propositional formula in the correct format
	 */
	public Formula(String input) {
		
		clauses = new ArrayList<>();
		literalValues = new HashMap<>();
		literalOccurences = new HashMap<>();
		clausesPropagated = new HashSet<>();
		
		translate(input);
		updateHeuristic();
	}
	
	/**
	 * Clause-form propopsitional formula
	 * @param f a formula to create a deep-copy of
	 */
	public Formula(Formula f) {
		
		this.clauses = new ArrayList<>();
		
		for (HashSet<String> clause : f.clauses) {
			clauses.add(new HashSet<>(clause));
		}

		this.literalValues = new HashMap<>(f.literalValues);
		this.literalOccurences = new HashMap<>(f.literalOccurences);
		this.clausesPropagated = new HashSet<>();
		
		updateHeuristic();
	}
	
	private void translate(String input) {
		
		String formula = input.substring(1, input.length()-1);
		String temp = "";
		int c = 0;
		
		// creates clauses
		for (int i = 0; i < formula.length(); i++) {
			
			if (formula.charAt(i) == '}') {
				
				String[] clause = temp.split(",");
				for (int j = 0; j < clause.length; j++) {
					clause[j] = clause[j].strip();
				}
				
				clauses.add(new HashSet<>(Set.of(clause)));
				temp = "";
				c--;
			}
			else if (formula.charAt(i) == '{') {
				c++;
			}
			else if (c > 0) {
				temp += formula.charAt(i);
			}
		}
		
		int value = 1;
		
		// creates clausesValue
		for (HashSet<String> clause : clauses) {
			
			for (String literal : clause) {
				
				if (literal.contains("-")) {
					literal = literal.substring(1);
				}
				
				if (!literalValues.containsKey(literal)) {
					literalValues.put(literal, value);
					literalValues.put("-" + literal, -value);		
					value++;
				}
			}
		}
		
	}
	
	public void updateHeuristic() {
		
		literalOccurences.clear();
		
		for (HashSet<String> clause : clauses) {
			for (String literal : clause) {
				
				if (literal.contains("-")) {
					literal = literal.substring(1);
				}
				
				if (literalOccurences.containsKey(literal)) {
					int occurences = literalOccurences.get(literal);
					literalOccurences.replace(literal, occurences + 1);
				}
				else {
					literalOccurences.put(literal, 1);
				}
			}
		}
	}
	
	public void removeLiteral(Integer l, HashSet<String> clause) {
		for (String literal : clause) {
			if (literalValue(literal) == l) {
				clause.remove(literal);
				return;
			}
		}
	}
	
	public Integer literalValue(String l) {
		if (literalValues.containsKey(l)) {
			return literalValues.get(l);
		}
		
		return 0;
	}
	
	public HashSet<String> remainingLiterals() {
		
		HashSet<String> temp = new HashSet<>();
		
		for (HashSet<String> clause : clauses) {
			temp.addAll(clause);
		}
		
		return temp;
	}
	
	@Override
	public String toString() {
		return "formula: " + clauses;
	}
}

class DPLL {
	
	/**
	 * 
	 * @param f
	 * @param index
	 * @return
	 */
	public String prove(Formula f, int index) {
		
		String s = "";
		for (int i = 0; i < f.toString().length(); i++) {
			s += "=";
		}
		
		System.out.println(s + " " + index);
		System.out.println(f);
		
		// unsatisfiable
		if (isAxiom(f)) {
			System.out.println("* axiom!");
			return "branch #" + index + ": unsatisfiable " + f.remainingLiterals();
		}
		
		boolean onlyUnitClauses = true;
		for (HashSet<String> clause : f.clauses) {
			if (!isUnitClause(clause, f)) {
				onlyUnitClauses = false;
			}
		}
		
		// satisfiable
		if (onlyUnitClauses) {
			System.out.println("* interpretation!");
			return "branch #" + index + ": satisfiable " + f.remainingLiterals();
		}
		
		// Unit Propagation
		ArrayList<HashSet<String>> copy = new ArrayList<>(f.clauses);
		for (HashSet<String> clause : copy) {
			
			// check if unit propagation is possible
			if (isUnitClause(clause, f) && !f.clausesPropagated.contains(clause)) {
				f.clausesPropagated.add(clause);
				propagate(clause, f);
				
				// back to start
				return prove(f, index);
			}
		}
		
		// Atomic cut
		return cut(f, index);
	}
	
	/**
	 * 
	 * @param unitClause
	 * @param f
	 */
	private void propagate(HashSet<String> unitClause, Formula f) {
		
		System.out.println("* propagate! " + unitClause);
		
		String literal = unitClauseLiteral(unitClause);
		int literalValue = f.literalValue(literal);
		
		ArrayList<HashSet<String>> clausesCopy = new ArrayList<>(f.clauses);
		clausesCopy.remove(unitClause);
		
		for (HashSet<String> clause : clausesCopy) {
			
			if (clause.contains(literal)) {
				f.clauses.remove(clause);
			}
			
			HashSet<String> temp = null;
			for (String cLiteral : clause) {
				if (-f.literalValue(literal) == f.literalValue(cLiteral)) {
					int cIndex = f.clauses.indexOf(clause);
					temp = f.clauses.get(cIndex);
				}
			}
			
			if (temp != null) {
				f.removeLiteral(-literalValue, temp);
			}
		}
	}
	
	/**
	 * 
	 * @param f
	 * @return
	 */
	private String cut(Formula f, int index) {
		
		f.updateHeuristic();
		
		HashSet<String> unitClauseLiterals = new HashSet<>();

		int max = 0;
		String cut = "";
		
		for (Entry<String, Integer> v : f.literalOccurences.entrySet()) {
			if (!unitClauseLiterals.contains(v.getKey()) && v.getValue() > max) {
				cut = v.getKey();
				max = v.getValue();
			}
		}
		
		System.out.println("* cut! " + cut + " " + f.literalOccurences);
		
		String negCut = "-" + cut;

		Formula f1 = new Formula(f);
		HashSet<String> newClause = new HashSet<>();
		newClause.add(cut);
		f1.clauses.add(newClause);

		Formula f2 = new Formula(f);
		newClause = new HashSet<>();
		newClause.add(negCut);
		f2.clauses.add(newClause);
		
		// for prettier output
		String s = "";
		
		System.out.println();
		s += "\n" + prove(f1, index * 2);
		
		System.out.println();
		s += "\n" + prove(f2, (index * 2) + 1);
		
		return s;
	}
	
	/**
	 * 
	 * @param f
	 * @return
	 */
	private boolean isAxiom(Formula f) {
		
		for (HashSet<String> clauseA : f.clauses) {
			
			ArrayList<HashSet<String>> copy = new ArrayList<>(f.clauses);
			copy.remove(clauseA);
			
			for (HashSet<String> clauseB : copy) {
				
				int literalValueA = f.literalValue(unitClauseLiteral(clauseA));
				int literalValueB = f.literalValue(unitClauseLiteral(clauseB));
				
				if (literalValueA == -literalValueB && literalValueA != 0) {
					System.out.println(clauseA + " " + clauseB);
					return true;
				}
			}
		}
		
		return false;
	}
	
	/**
	 * 
	 * @param c
	 * @param f
	 * @return
	 */
	private boolean isUnitClause(HashSet<String> c, Formula f) {
		return f.literalValue(unitClauseLiteral(c)) != 0;
	}
	
	/**
	 * 
	 * @param c
	 * @return
	 */
	private String unitClauseLiteral(HashSet<String> c) {
		if (c.size() == 1) {
			return c.toArray()[0].toString();
		}
		return "";
	}

}
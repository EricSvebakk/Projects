import java.io.File;
import java.util.Arrays;
import java.util.HashSet;

// import testing.BCNF2;

public class RDBTesting {
	
	public static void main(String[] args) {
		
		RDB r = new RDB(new File("testing/julie_data.txt"));
		
		System.out.println(r);
		
		
		
		// for (String ck : r.RDB_CKs) {
		// 	System.out.println(ck + " " + r.getClosure(ck, r.RDB_FDs));
		// }
		
		// HashMap<String, String> FDs = new HashMap<>();
		// FDs.put("BCF", "D");
		// System.out.println("**** " + r.findNFs(FDs, r.RDB_CKs));
		
		// r.decompose("A");
		
		
		System.out.println("CLOSURE");
		
		String l = "NKA";
		// String combos = r.
		String result = r.getClosure(l, r.RDB_FDs);
		
		System.out.println("FDs: " + r.RDB_FDs);
		System.out.println("result ("+ l +"): " + result);
		
		
		
		HashSet<String> stuff = new HashSet<>();
		
		stuff.add("a");
		stuff.add("b");
		stuff.add("c");
		
		String res = String.join("", stuff);
		
		System.out.println(res);
		
		HashSet<String> s = new HashSet<>(Arrays.asList(res.split("")));
		
		System.out.println("result: " + s);
	}
}

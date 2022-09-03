import java.io.File;

public class RDBTesting {
	
	public static void main(String[] args) {
		
		RDB r = new RDB(new File("testing/fungerendeeksempel.txt"));
		
		System.out.println(r);
		
		for (char s : r.RDB_A.toCharArray()) {
			System.out.println(s + " " + r.getClosure(String.valueOf(s), r.RDB_FDs));
		}
		System.out.println("\n================================");
		
		// for (String ck : r.RDB_CKs) {
		// 	System.out.println(ck + " " + r.getClosure(ck, r.RDB_FDs));
		// }
		
		// HashMap<String, String> FDs = new HashMap<>();
		// FDs.put("BCF", "D");
		// System.out.println("**** " + r.findNFs(FDs, r.RDB_CKs));
		
		r.decompose("CDE");
	}
}

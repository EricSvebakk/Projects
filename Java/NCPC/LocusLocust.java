
import java.io.BufferedReader;
import java.util.HashMap;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class LocusLocust {
	
	public static void main(String[] args) {
		
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		PrintWriter writer = new PrintWriter(System.out);
		
		int lim;
		try {
			lim = Integer.parseInt(br.readLine());
		} catch (IOException e) {
			lim = 0;
		}
		
		HashMap<Integer, Integer> data = new HashMap<>();
		String[] bits;
		
		for (int i = 0; i < lim; i++) {
			
			try {
				bits = br.readLine().split(" ");
			} catch (IOException e) {
				bits = null;
			}
			
			data.put(Integer.parseInt(bits[0]), Integer.parseInt(bits[1])*Integer.parseInt(bits[2]));
		}
		
		int result = 99999999;
		int i;
		int t; 
		
		
		for(int k : data.keySet()) {
			t = 0;
			i = 0;
			// System.out.println("");
			
			while (t < 2022) {
				
				t = k + (data.get(k) * i);
				
				if ((t < result) && (t >= 2022)) {
					result = t;
				} 
				
				i++;
				// System.out.println(t);
			}
		}
		
		System.out.println(result);
	}
}
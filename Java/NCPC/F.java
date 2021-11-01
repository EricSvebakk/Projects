

public class F {

	public static void main(String[] args) {
		
		
		// System.out.println(MyMath.fac(10));
		// System.out.println(MyMath.binom(10,8));
		// System.out.println(MyMath.binomDistribution(10, 5, 0.5));
		
		double p = 0.0026;
		double n = MyMath.binomDistribution(6, 1, p);
		
		System.out.println((p*(1-p)) / n + " " + n);
		
		
		// double i = 0;
		// int j = 0;A
		
		// while (i < 1) {
		// 	i += n;
		// 	j++;
		// }
		
		// System.out.println(j);
		
		// System.out.println(1/MyMath.binomDistribution(6, 1, 0.0026));
		// System.out.println(1/MyMath.binomDistribution(3, 2, 0.0026));
	}
}

// 5.922404546810213463068107497132
class MyMath {
	
	public static long fac(int n) {
		
		long fac = 1;
		for (int i = 1; i <= n; i++) {
			fac *= i;			
		}
		return fac;
	}
	
	public static double binom(int n, int k) {
		return fac(n) / (fac(k) * fac(n-k));	
	}
	
	public static double binomDistribution(int n, int k, double p) {
		return binom(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
	}
}
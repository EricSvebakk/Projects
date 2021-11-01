
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

public class Food {

	public static void main(String[] args) {
		
		// 
		Scanner fs;
		Scanner rs;
		
		// 
		try {
			fs = new Scanner(new File("food.tsv"));
			rs = new Scanner(new File("recipes.tsv"));
		}
		catch (FileNotFoundException e) {
			return;
		}
		
		HashSet<String> foodAvailable = new HashSet<>();
		HashMap<Recipe, Boolean> recipes = new HashMap<>();
		
		while (fs.hasNextLine()) {
			foodAvailable.add(fs.nextLine().strip().replace("_", " "));
		}
		
		while (rs.hasNextLine()) {
			
			HashMap<String, Boolean> ingredients = new HashMap<>();
			String[] data = rs.nextLine().split("\t");
			String name = data[0].replace("_", " ");
			
			for (int i = 1; i < data.length; i++) {
				ingredients.put(data[i].replace("_"," "), false);
			}
			
			recipes.put(new Recipe(name, ingredients), false);
		}
		
		
		System.out.println(foodAvailable);
		
		for (String i : foodAvailable) {
			for (Recipe r : recipes.keySet()) {
				
				if (r.needIngredients.containsKey(i)) {
					r.needIngredients.replace(i, true);
				}
			}
		}
		
		
		System.out.println();
		for (Recipe r : recipes.keySet()) {
			if (r.canEat()) {
				System.out.println(r);
			}
		}
		
		
		fs.close();
		rs.close();
	}

}

class Recipe {
	
	String name;
	HashMap<String, Boolean> needIngredients;
	
	public Recipe(String n, HashMap<String, Boolean> i) {
		this.name = n;
		this.needIngredients = i;
	}
	
	public Boolean canEat() {
		for (Boolean i : needIngredients.values()) {
			if (!i) {
				return false;
			}
		}
		
		return true;
	}
	
	public String toString() {
		
		// String s = "\n" + name + ":\n";
		// for (String i : ingredients.keySet()) {
		// 	s += "- " + i + "\n";
		// }
		
		// for (Boolean i : needIngredients.values()) {
		// 	if (!i) {
		// 		return "\n" + name + ":\n- Unavailable\n";
		// 	}
		// }
		
		// return "\n" + name + ":\n- Available\n";
		
		return name + "\n";
	}
}

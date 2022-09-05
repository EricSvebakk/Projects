import java.util.ArrayList;

public class SortRute extends Rute {
    
    public SortRute(int x, int y, Labyrint l) {
        super(x, y, l);
    }
    
    // unicode symbol for hvit firkant
    @Override
    public String toString() {
        return "\u25A0";
    }
    
    // ikke brukt
    public char tilTegn() {
        return '#';
    }
    
    // Ingen skjer dersom stien kommer til en sort rute
    public void gaa(ArrayList<Tuppel> sti) {
        // trist
    }
}

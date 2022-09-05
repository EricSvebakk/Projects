import java.util.ArrayList;

public class Aapning extends HvitRute {
    
    public Aapning(int x, int y, Labyrint l) {
        super(x, y, l);
    }
    
    @Override
    public String toString() {
        return ".";
    }
    
    // Stopper sti og lagrer den som en ny utvei
    @Override
    public void gaa(ArrayList<Tuppel> sti) {
        Tuppel temp = new Tuppel(x, y);
        sti.add(temp);
        labyrint.leggTilUtvei(sti);
    }
}

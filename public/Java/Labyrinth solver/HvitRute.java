
import java.util.ArrayList;

public class HvitRute extends Rute {
    
    public HvitRute(int x, int y, Labyrint l) {
        super(x, y, l);
    }
    
    @Override
    public String toString() {
        return " ";
    }
    
    // ikke brukt
    public char tilTegn() {
        return '.';
    }
    
    // rekursiv metode for traversering av labyrint
    public void gaa(ArrayList<Tuppel> sti) {
        
        Tuppel temp = new Tuppel(x, y);
        sti.add(temp);
        
        // Henter nabp-ruter
        naboLoop:
        for (int i = 0; i < 4; i++) {
            
            // Sjekker at en sti eksisterer
            if (sti.size() > 1) {
                
                // Henter ut ruter i stien
                for (int j = 0; j < sti.size(); j++) {
                    boolean likX = sti.get(j).hentX() == naboer[i].hentX();
                    boolean likY = sti.get(j).hentY() == naboer[i].hentY(); 
                    
                    // Ignorerer denne nabo-ruten dersom den fins i stien allerede
                    if (likX && likY)
                        continue naboLoop;
                }
            }
            
            // Nåværende sti sendes videre til neste rute
            ArrayList<Tuppel> nySti = new ArrayList<>(sti);
            naboer[i].gaa(nySti);
        }
    }
}

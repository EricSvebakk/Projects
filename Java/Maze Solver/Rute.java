
import java.util.ArrayList;

abstract public class Rute {
    
    protected int x;
    protected int y;
    protected Labyrint labyrint;
    protected Rute[] naboer = new Rute[4];
    
    public Rute(int x, int y, Labyrint l) {
        this.x = x;
        this.y = y;
        this.labyrint = l;
    }
    
    // Henter x-posisjon
    public int hentX() {
        return x;
    }
    
    // Henter y-posisjon
    public int hentY() {
        return y;
    }
    
    // Oppdaterer nabo-liste med kardinale naboer
    public void finnNaboer() {
        
        int xi = -1;
        int yi = -1;
        int i = 0;
        while (yi < 2) {
            
            // Ignorerer hjørne-naboer
            if (Math.abs(xi - yi) == 1) {
                boolean grenseX = (x + xi < labyrint.hentAntX()) && (x + xi >= 0);
                boolean grenseY = (y + yi < labyrint.hentAntY()) && (y + yi >= 0);
                
                // Ignorerer posisjoner utenfor rutenett
                if (grenseX && grenseY)
                    naboer[i] = labyrint.hentRute(xi+x, yi+y);
                    i++;
            }
            
            xi++;
            if (xi > 1) {
                xi = -1;
                yi++;
            }
        }
        
    }
    
    // Nyttig til debugging
    public Rute[] hentNaboer() {
        
        System.out.print("(");
        for (int i = 0; i < 4; i++) {
            System.out.print(naboer[i] + ",");
        }
        System.out.println(")");
        
        return naboer;
    }
    
    // Oppretter liste av utveier og kjører gaa()
    public void finnUtvei() {
        ArrayList<Tuppel> sti = new ArrayList<Tuppel>();
        this.gaa(sti);
    }
    
    abstract public void gaa(ArrayList<Tuppel> sti);
    abstract public char tilTegn();
}
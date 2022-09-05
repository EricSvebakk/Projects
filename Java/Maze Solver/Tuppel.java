
public class Tuppel {

    private int x;
    private int y;
    
    // Uforanderlig lagringsobjekt
    Tuppel(int x, int y) {
        this.x = x;
        this.y = y;
    }
    
    // Henter ut x-verdi
    public int hentX() {
        return x;
    }
    
    // Henter ut y-verdi
    public int hentY() {
        return y;
    }
    
    public String toString() {
        return "(" + x + "," + y + ")";
    }
    
}

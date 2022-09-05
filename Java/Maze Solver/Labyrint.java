
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class Labyrint {
    
    protected boolean finUtskrift = false;
    protected Scanner scanner;
    protected int antX;
    protected int antY;
    protected Rute[][] rutenett;
    protected ArrayList<ArrayList<Tuppel>> utveier = new ArrayList<>();
    
    // Standard konstruktør trenger kun fil
    public Labyrint(File fil) throws FileNotFoundException {
        this.scanner = new Scanner(fil);
        lagLabyrint(scanner);
    }
    
    // Overloaded konstruktør for å skru på utskriftsinformasjon
    public Labyrint(File fil, boolean finUtskrift) throws FileNotFoundException {
        this.scanner = new Scanner(fil);
        this.finUtskrift = finUtskrift;
        lagLabyrint(scanner);
    }
    
    // Privat metode som kalles av konstruktører for å opprette rutenett
    private void lagLabyrint(Scanner scanner) {
        
        String linje;
        int xi = 0;
        int yi = 0;
        antY = scanner.nextInt();
        antX = scanner.nextInt();
        rutenett = new Rute[antX][antY];
        
        // While-løkke til lesing av fil-data
        while (scanner.hasNext()) {

            // Oversette String til char-array
            linje = scanner.next();
            char[] chars = linje.toCharArray();

            // Oppretter ulike ruter og legger dem til i rutenettet
            for (char c : chars) {
                if (c == '#')
                    rutenett[xi][yi] = new SortRute(xi, yi, this);
                else if (xi == (antX - 1) || yi == (antY - 1) || xi == 0 || yi == 0)
                    rutenett[xi][yi] = new Aapning(xi, yi, this);
                else
                    rutenett[xi][yi] = new HvitRute(xi, yi, this);
                xi++;
            }

            xi = 0;
            yi++;
        }
        scanner.close();
        
        // Oppdaterer alle ruter i rutenettet med nabo-oversikt
        for (yi = 0; yi < antY; yi++) {
            for (xi = 0; xi < antX; xi++) {
                rutenett[xi][yi].finnNaboer();
            }
        }
        
        // Skriver ut labyrintens dimensjoner og en representasjon
        if (finUtskrift) {
            System.out.println("\nlagLabyrint: rutenett opprettet!");
            System.out.println("lagLabyrint: dimensjoner = " + antX + "x" + antY);
            System.out.println("\n" + this);
        }
    }
    
    // Antall ruter langs x-aksen
    public int hentAntX() {
        return antX;
    }
    
    // Antall ruter langs y-aksen
    public int hentAntY() {
        return antY;
    }
    
    // Nyttig til debugging 
    public void hentNaboer(int x, int y) {
        rutenett[x][y].hentNaboer();
    }
    
    // henter en angitt rute fra rutenettet
    // Burde brukes med hentAntX og hentAntY
    public Rute hentRute(int x, int y) {
        return rutenett[x][y];
    }
    
    // Oppdaterer liste av utveier med en ny utvei
    public void leggTilUtvei(ArrayList<Tuppel> utvei) {
        utveier.add(utvei);
    }
    
    // 
    public ArrayList<ArrayList<Tuppel>> hentUtveier() {
       return utveier; 
    }
    
    // Traverserer gjennom labyrint og finner alle utveier fra en angitt posisjon
    public ArrayList<ArrayList<Tuppel>> finnUtveiFra(int x, int y) {
        
        utveier.clear();
        rutenett[x][y].finnUtvei();
        
        // Sjekker om en sti finnes
        if (utveier.size() != 0) {
            int kortestUtvei = 0;
            int i = 0;
            
            // Henter ut alle utveier
            for (ArrayList<Tuppel> u : utveier) {

                // Printer uten en representasjon av hver sti
                if (finUtskrift) {
                    
                    System.out.println("Utvei #" + i);
                    
                    for (int yi = 0; yi < antY; yi++) {
                        xLoop:
                        for (int xi = 0; xi < antX; xi++) {
                            
                            // Sammenligner ruter i rutenett med ruter i utvei
                            for (Tuppel t : u) {
                                if (xi == t.hentX() && yi == t.hentY()) {
                                    System.out.print(". ");
                                    continue xLoop;
                                }
                            }
                            System.out.print(rutenett[xi][yi] + " ");
                        }
                        System.out.println();
                    }
                    
                    // Start og slutt rute
                    System.out.println(u.get(0) + " -> " + u.get(u.size() - 1) + "\n\n\n");
                    
                    // Oppdaterer kortestUtvei 
                    if (u.size() < utveier.get(kortestUtvei).size()) {
                        kortestUtvei = i;
                    }
                    
                    i++;
                    System.out.println("ANTALL UTVEIER: " + utveier.size());
                    System.out.println("KORTEST UTVEIER ER #" + kortestUtvei + ": "+ utveier.get(kortestUtvei).size() + " RUTER \n\n");
                }
                
            }
            
        }
        
        // Varsel dersom ingen sti er funnet
        else
            System.out.println("Ingen utvei funnet!\n\n");
        
        // System.out.println(utveier);
            
        return utveier;
    }
    
    public String toString() {
        String s = "";
        for (int yi = 0; yi < antY; yi++) {
            for (int xi = 0; xi < antX; xi++) {
                s += rutenett[xi][yi] + " ";
            }
            s += "\n";
        }
        return s;
    }
}
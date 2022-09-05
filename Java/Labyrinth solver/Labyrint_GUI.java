
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.LineBorder;

import java.io.File;
import java.io.FileNotFoundException;

import java.util.ArrayList;

public class Labyrint_GUI {
    
    private Labyrint labyrint;
    private RuteKnapp[][] knappRutenett;
    private ArrayList<Tuppel> synligUtvei;
    
    private int stiTeller = 1;
    private int antStiMin = 0;
    private int antStiMaks = 0;
    
    private TellerKnapp forrige;
    private TellerKnapp neste;
    private JFrame vindu;
    private JPanel panelRuter;
    private JPanel panelInfo;
    private JLabel tekstTeller;
    private JLabel tekstLengde;
    
    private Color bgFarge = Color.LIGHT_GRAY;
    
    // 
    public Labyrint_GUI(JFrame v) {
        this.vindu = v;
        this.panelInfo = new JPanel();
        this.panelRuter = new JPanel();
        
        // 
        panelInfo.setBackground(bgFarge);
        panelInfo.setPreferredSize(new Dimension(200, 600));
        vindu.add(panelInfo);

        //
        panelRuter.setBackground(Color.WHITE);
        panelRuter.setPreferredSize(new Dimension(600, 600));
        panelRuter.setBorder(new LineBorder(bgFarge, 10));
        // Border border = ;
        // panel.setBorder(border);
        vindu.add(panelRuter);
        
        lagGUI();
    }
    
    // 
    public void lagGUI() {
        
        FilKnapp filKnapp = new FilKnapp("velg fil", this);
        forrige = new TellerKnapp("-1", -1, this, tekstTeller);
        neste = new TellerKnapp("+1", 1, this, tekstTeller);
        tekstTeller = new JLabel("0 / 0");
        tekstLengde = new JLabel();
        
        GridBagConstraints gbc = new GridBagConstraints();
        panelInfo.setLayout(new GridBagLayout());
        gbc.insets = new Insets(3, 3, 3, 3);
        gbc.fill = GridBagConstraints.NONE;
        gbc.anchor = GridBagConstraints.CENTER;
        
        gbc.gridx = 0;
        gbc.gridy = 0;
        panelInfo.add(forrige, gbc);
        
        gbc.gridx = 1;
        gbc.gridy = 0;
        panelInfo.add(tekstTeller, gbc);
        
        gbc.gridx = 2;
        gbc.gridy = 0;
        panelInfo.add(neste, gbc);
        
        gbc.gridx = 1;
        gbc.gridy = 1;
        panelInfo.add(filKnapp, gbc);
        
        gbc.gridx = 1;
        gbc.gridy = 2;
        panelInfo.add(tekstLengde, gbc);
    }
    
    // 
    public void lagLabyrint(File fil) {
        
        panelRuter.removeAll();
        panelRuter.setBackground(bgFarge);
        panelRuter.repaint();
        synligUtvei = null;
        knappRutenett = null;
        
        this.endreStiTeller(-stiTeller);
        antStiMaks = 0;
        stiTeller = 0;
        
        try {
            labyrint = new Labyrint(fil);
        }
        catch (FileNotFoundException e) {
            System.out.printf("Filen '%s' ikke funnet!\n", fil);
            System.exit(1);
        }
        
        int antX = labyrint.hentAntX();
        int antY = labyrint.hentAntY();
        
        knappRutenett = new RuteKnapp[antX][antY];
        panelRuter.setLayout(new GridLayout(antY, antX));

        for (int yi = 0; yi < antY; yi++) {
            for (int xi = 0; xi < antX; xi++) {
                RuteKnapp knapp = new RuteKnapp(xi, yi, this);
                knapp.setBorderPainted(false);
                knappRutenett[xi][yi] = knapp;
                panelRuter.add(knapp);
            }
        }

        vindu.validate();
    }
    
    // 
    public Labyrint hentLabyrint() {
        return labyrint;
    }
    
    // 
    public JLabel hentTekstLengde() {
        return tekstLengde;
    }
    
    // 
    public RuteKnapp[][] hentKnapper() {
        return knappRutenett;
    }
    
    public void settAntStiMaks(int nyMaks) {
        antStiMaks = nyMaks;
    }
    
    // 
    public int hentAntStiMaks() {
        return antStiMaks;
    }
    
    //
    public int hentAntStiMin() {
        return antStiMin;
    }
    
    //
    public void endreStiTeller(int endring) {
        stiTeller += endring;
        tekstTeller.setText(stiTeller + " / " + antStiMaks);
    }

    //
    public int hentStiTeller() {
        return stiTeller;
    }
    
    //
    public void settValgtUtvei(ArrayList<Tuppel> nyUtvei) {
        synligUtvei = nyUtvei;
    }
    
    // 
    public void visValgtUtvei() {
        boolean forste = true;
        for (Tuppel t : synligUtvei) {
            if (forste) {
                knappRutenett[t.hentX()][t.hentY()].setBackground(Color.MAGENTA);
            } else {                
                knappRutenett[t.hentX()][t.hentY()].setBackground(Color.CYAN);
            }
            forste = false;
        }
    }
    
    // 
    public void fjernValgtUtvei() {
        if (synligUtvei != null) {
            for (Tuppel t : synligUtvei) {
                RuteKnapp rute = knappRutenett[t.hentX()][t.hentY()];
                rute.setBackground(rute.hentFarge());
            }
        }
    }
    
}

//
class RuteKnapp extends JButton {

    private int x;
    private int y;
    private Labyrint_GUI gui;
    private Labyrint labyrint;
    private Color farge;

    public RuteKnapp(int x, int y, Labyrint_GUI gui) {
        this.x = x;
        this.y = y;
        this.gui = gui;
        this.labyrint = gui.hentLabyrint();
        
        if (labyrint.hentRute(x, y).tilTegn() == '#') {
            this.farge = Color.BLACK;
        } else {
            this.farge = Color.WHITE;
        }
        
        setBackground(farge);
        initGUI();
    }

    //
    class Handling implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {

            gui.fjernValgtUtvei();

            //
            if (labyrint.finnUtveiFra(x, y).size() > 0) {
                
                ArrayList<ArrayList<Tuppel>> utveier = labyrint.hentUtveier();
                ArrayList<Tuppel> kortestUtvei = utveier.get(0);
                int kortestUtveiIndeks = 0;
                
                for (ArrayList<Tuppel> al : utveier) {
                    if (al.size() < kortestUtvei.size()) {
                        kortestUtvei = al;
                    }
                }
                
                gui.settAntStiMaks(utveier.size());
                gui.endreStiTeller(-gui.hentStiTeller() + 1);
                
                if (kortestUtvei != null) {
                    kortestUtveiIndeks = labyrint.hentUtveier().indexOf(kortestUtvei);
                    gui.endreStiTeller(kortestUtveiIndeks);
                    gui.settValgtUtvei(kortestUtvei);
                    gui.visValgtUtvei();
                }
                
                gui.hentTekstLengde().setText("Lengde: " + kortestUtvei.size());

            } else {
                gui.settValgtUtvei(null);
                gui.hentTekstLengde().setText("");
                gui.endreStiTeller(-gui.hentStiTeller());
                gui.settAntStiMaks(0);
            }
        }
    }

    //
    public Color hentFarge() {
        return farge;
    }

    //
    public void initGUI() {
        addActionListener(new Handling());
    }
}

//
class TellerKnapp extends JButton {

    private Labyrint_GUI gui;
    private int endring;

    //
    public TellerKnapp(String t, int e, Labyrint_GUI gui, JLabel tf) {
        super(t);
        this.endring = e;
        this.gui = gui;
        initGUI();
    }

    //
    class Handling implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {

            Labyrint labyrint = gui.hentLabyrint();
            int teller = gui.hentStiTeller();
            int maks = gui.hentAntStiMaks();
            int min = gui.hentAntStiMin();
            
            //
            if (teller + endring > min && teller + endring <= maks) {
                
                gui.endreStiTeller(endring);
                ArrayList<Tuppel> utvei = labyrint.hentUtveier().get(gui.hentStiTeller() - 1);
                
                gui.fjernValgtUtvei();
                gui.settValgtUtvei(utvei);
                gui.visValgtUtvei();
                
                gui.hentTekstLengde().setText("Lengde: " + utvei.size());
            }
        }
    }

    //
    public void initGUI() {
        addActionListener(new Handling());
    }
}

// 
class FilKnapp extends JButton {
    
    private Labyrint_GUI gui;
    private JFileChooser velger = null;
    
    public FilKnapp(String t, Labyrint_GUI gui) {
        super(t);
        this.gui = gui;
        initGUI();
    }
    
    class Handling implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            
            velger = new JFileChooser();
            velger.setCurrentDirectory(new java.io.File("."));
            int resultat = velger.showOpenDialog(null);
            if (resultat != JFileChooser.APPROVE_OPTION) {
                return;
            }
            
            gui.lagLabyrint(velger.getSelectedFile());
        }
    }
    
    public void initGUI() {
        addActionListener(new Handling());
    }
    
}
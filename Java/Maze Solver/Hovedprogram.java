
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Hovedprogram {
    
    public static void main(String[] args) {
        
        // 
        JFrame vindu = new JFrame("Labyrint");
        vindu.setLayout(new GridBagLayout());
        vindu.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        vindu.setResizable(false);
        
        // // 
        // JPanel panelInfo = new JPanel();
        // panelInfo.setBackground(Color.GREEN);
        // panelInfo.setPreferredSize(new Dimension(200, 600));
        // vindu.add(panelInfo);
        
        // // 
        // JPanel panelRuter = new JPanel();
        // panelRuter.setBackground(new Color(255, 0, 255));
        // panelRuter.setPreferredSize(new Dimension(600, 600));
        // vindu.add(panelRuter);
        
        Labyrint_GUI gui = new Labyrint_GUI(vindu);
        
        //  
        vindu.pack();
        vindu.setVisible(true);
    }
    
}



var tegn, bui;

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
window.onload = () => {
    tegn = new canvasGRID("canvas", 600, 600, true, 0, 0, 20, 20);
    bui = new betterUI("container", false, 200);

    bui.text(["terninger","kast"]);
    bui.bttn(["Go"], "container_form_input")
    
    $setClick("Go",terningkast);
}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
function terningkast() {
    console.clear();

    // Variabler
    let kast = parseInt($getVal("kast")),
        terninger = parseInt($getVal("terninger")),
        tilfeldig = undefined,
        verdier = {};

    for (let i = 1; i < (terninger * 6) + 1; i++) verdier[i.toString()] = 0;

    for (let i = 0; i < kast; i++) {
        tilfeldig = 0;
        for (let j = 0; j < terninger; j++) tilfeldig += randomNumber(1, 6);
        for (let j = 1; j < (terninger * 6) + 1; j++) if (j == tilfeldig) verdier[j.toString()]++;
    }

    // Tegner datasett i graf
    tegn.blankCanvas();
    tegn.barGraph(0, 0, 20, 20, verdier, 0.1);
    tegn.grid();
}
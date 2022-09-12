
var tegn, bui;

var results = {
    /* "extraverted": {
        2016: 32,
        2018: 78,
        2019: 74,
        2020: 58,
        2021: 100
    }, */
    "intuitive": {
        2016: 59,
        2018: 63,
        2019: 59,
        2020: 76,
        2021: 35,
        2022: 45
    },
    /* "feeling": {
        2016: 56,
        2018: 64,
        2019: 56,
        2020: 83,
        2021: 20
    }, */
    /* "prospecting": {
        2016: 55,
        2018: 44,
        2019: 44,
        2020: 58,
        2021: 41
    }, */
    /* "turbulent": {
        2016: 73,
        2018: 47,
        2019: 53,
        2020: 75,
        2021: 56
    }, */
};

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
window.onload = () => {
    tegn = new canvasGRID("canvas", 600, 600, 0, 0, 20, 20);
    bui = new betterUI(false, 200);

    bui.text(["terninger", "kast"]);
    $setClick("form_button", terningkast);
    terningkast();
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

    console.log(Object.keys(results).length);
    console.log(Object.values(results));
    console.log(Object.values(results)[0]);
    console.log(Object.values(results)[0][2016]);

    // Tegner datasett i graf
    tegn.clearCanvas();
    
    tegn.lineGraph(0, 0, 20, 20, results);
    //tegn.barGraph(0, 0, 20, 20, verdier);
    /* tegn.grid(); */
}






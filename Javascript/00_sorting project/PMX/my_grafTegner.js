
//=====================================//
// fyller inn fargen under en funksjon //
//=====================================//
function tegnFunksjonFyll(matFunksjon,farge) {

    var deltaXn = 0.0025;

    var xn1 = x1 + deltaXn;
    var xn2 = xn1 + deltaXn;
    var yn1;
    var yn2;

    for (var i = x1; i < x2 - deltaXn; i += deltaXn) {

        yn1 = y1
        yn2 = matFunksjon(i);

        if (xn1 > x1) {xn1 += deltaXn}
        if (xn2 < x2) {xn2 += deltaXn}

        e2d.fillRectangle(xn1,yn1,xn2,yn2,farge);
    }
}

//====================================//
// tegner inn enn aksene inn i canvas //
//====================================//
function akseTegner(idTTL, desimalX = 2, desimalY = 2, viskut = true) {
    
    let umc = [x1,x2,y1,y2],
        ncc = [0.01,1,0,0.85],
        tekster = [idTTL,"x-akse","y-akse"]

    // Definerer koordinattransformasjoner
    if (umc.length < 4 || ncc.length < 4 || tekster.length < 3) console.log("tegnUMCAkser--> Feil arraydata !");

    e2d.xRange(umc[0], umc[1]); 	// 1.aksens begrensninger
    e2d.yRange(umc[2], umc[3]); 	// 2.aksens begrensninger
    e2d.viewport(ncc[0], ncc[1], ncc[2], ncc[3]);
    if (viskut) e2d.clearCanvas();
    e2d.drawBoundary();
    
    umc[0] = 0; umc[1] = 10;
    umc[2] = 0; umc[3] = 10;

    // Tegner x-aksen
    var yLav = e2d.ucY1 - 0.015 * (e2d.ucY2 - e2d.ucY1);
    e2d.beginPath();
    niceX = finnPentIntervall(umc[0], umc[1]);
    for (x = niceX[0]; x <= niceX[1]; x = x + niceX[2]) {
        if (x >= e2d.ucX1 && x <= e2d.ucX2) {
            // e2d.moveTo(x,e2d.ucY1); e2d.lineTo(x,yLav);
            e2d.text(x, yLav, x.toFixed(desimalX), "black", "10px Arial", "center", "top");
        }
    }

    // Tegner y-aksen
    var xLav = e2d.ucX1 - 0.015 * (e2d.ucX2 - e2d.ucX1);
    niceY = finnPentIntervall(umc[2], umc[3]);
    for (y = niceY[0]; y <= niceY[1]; y = y + niceY[2]) {
        if (y >= e2d.ucY1 && y <= e2d.ucY2) {
            // e2d.moveTo(e2d.ucX1,y); e2d.lineTo(xLav,y);
            e2d.text(xLav, y, y.toFixed(desimalY), "black", "10px Arial", "right", "middle");
        }
    }

    e2d.stroke();
    // Tegner gridlinjer
    e2d.beginPath();
    e2d.context.lineWidth = 1;
    e2d.context.strokeStyle = "#888"; // uncommented by Eric, added "#888", removed color
    e2d.context.setLineDash([2, 3]);

    for (x = niceX[0]; x <= niceX[1]; x = x + niceX[2]) {
        if (x >= e2d.ucX1 && x <= e2d.ucX2) {
            e2d.moveTo(x, e2d.ucY1);
            e2d.lineTo(x, e2d.ucY2);
        }
    } // x-skritt linjer

    for (y = niceY[0]; y <= niceY[1]; y = y + niceY[2]) {
        if (y >= e2d.ucY1 && y <= e2d.ucY2) {
            e2d.moveTo(e2d.ucX1, y);
            e2d.lineTo(e2d.ucX2, y);
        }
    } // y-skritt linjer

    e2d.stroke();
    e2d.context.setLineDash([])
    var xm = (umc[0] + umc[1]) / 2;
    var ym = (umc[2] + umc[3]) / 2;
    e2d.text(xm, umc[3], tekster[1], "black", "16px Arial", "center", "bottom"); // Annotering 1.akse
    e2d.text(xm, umc[3] + (umc[3] - umc[2]) * 0.15, tekster[0], "black", "24px Arial", "center", "bottom"); // Tittel
    e2d.text(umc[1], ym, tekster[2], "black", "16px Arial", "center", "bottom", -90); // Annotering 2.akse
    // Tegner første- og andreaksen
    e2d.beginPath();

    if (e2d.ucY1 < 0 && e2d.ucY2 > 0) {
        e2d.moveTo(e2d.ucX1, 0);
        e2d.lineTo(e2d.ucX2, 0);
    } // y = 0 linje | null-linje

    if (e2d.ucX1 < 0 && e2d.ucX2 > 0) {
        e2d.moveTo(0, e2d.ucY1);
        e2d.lineTo(0, e2d.ucY2);
    }

    e2d.stroke();

}

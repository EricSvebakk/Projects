/*
	Formål:
		Verktøykasse for å definere og tegne et koordinatsystem. Anvendes både ved
		presentasjon av matematiske funksjoner og ved visualisering av data representert
		ved regulære grid eller punktskyer.

	Dette kodebiblioteket forutsetter at tegningen foregår i et easy2DGraphics objekt
    med navn e2d (Global variabel).

	Biblioteker som er benyttet:
		* easy2DGraphics

	Funksjoner i dette kodebiblioteket:
		* definere og tegne koordinatsystem

	FORUTSETNINGER:
		* Global variabel e2d eksisterer for easy2DGraphics grafikkbiblioteket.

    FRI INTERN BRUK PÅ FAGERLIA VGS,ÅLESUND (Rolf Magne Aasen)
	8.januar 2019
*/
// Forutsetning: window og viewport satt utenfor
function tegnAkserXY(tittel,tekstX="x-akse",tekstY="y-akse",desimalX=2,desimalY=2){
	var umc = [];
	umc[0]= e2d.ucX1;umc[1]= e2d.ucX2;umc[2]= e2d.ucY1;umc[3]= e2d.ucY2;

// Tegner x-aksen
	var yLav = e2d.ucY1-0.015*(e2d.ucY2-e2d.ucY1);
	e2d.beginPath();
	niceX = finnPentIntervall(umc[0],umc[1]);
	for (x=niceX[0];x<=niceX[1];x=x+niceX[2]){
		if (x >= e2d.ucX1 && x <= e2d.ucX2){
			// e2d.moveTo(x,e2d.ucY1); e2d.lineTo(x,yLav);
			e2d.text(x,yLav,x.toFixed(desimalX),"black", "10px Arial","center","top" );
		}
	}

// Tegner y-aksen
	var xLav = e2d.ucX1-0.015*(e2d.ucX2-e2d.ucX1);
	niceY = finnPentIntervall(umc[2],umc[3]);
	for (y=niceY[0];y<=niceY[1];y=y+niceY[2]){
		if (y >= e2d.ucY1 && y <= e2d.ucY2){
			// e2d.moveTo(e2d.ucX1,y); e2d.lineTo(xLav,y);
			e2d.text(xLav,y,y.toFixed(desimalY),"black", "10px Arial","right","middle");
		}
	}

	e2d.stroke();
	// Tegner gridlinjer
	e2d.beginPath();
	e2d.context.lineWidth = 1;
	e2d.context.strokeStyle = "#888"; // uncommented by Eric, added "#888", removed color
	e2d.context.setLineDash([2,3]);

	for (x=niceX[0];x<=niceX[1];x=x+niceX[2]){
		if (x >= e2d.ucX1 && x <= e2d.ucX2){
			e2d.moveTo(x,e2d.ucY1);
			e2d.lineTo(x,e2d.ucY2);
		}
	} // x-skritt linjer

	for (y=niceY[0];y<=niceY[1];y=y+niceY[2]){
		if (y >= e2d.ucY1 && y <= e2d.ucY2){
			e2d.moveTo(e2d.ucX1, y);
			e2d.lineTo(e2d.ucX2, y);
		}
	} // y-skritt linjer

	e2d.stroke();
	e2d.context.setLineDash([])
	var xm = (umc[0]+umc[1])/2;
	var ym = (umc[2]+umc[3])/2;
	e2d.text(xm,umc[3],tekstX,"black","16px Arial","center","bottom"); // Annotering 1.akse
	e2d.text(xm,umc[3]+(umc[3]-umc[2])*0.15,tittel,"black","24px Arial","center","bottom"); // Tittel
	e2d.text(umc[1],ym,tekstY,"black","16px Arial","center","bottom",-90); // Annotering 2.akse
	// Tegner første- og andreaksen
	e2d.beginPath();

	if (e2d.ucY1 < 0 && e2d.ucY2 > 0){
		e2d.moveTo(e2d.ucX1,0);
		e2d.lineTo(e2d.ucX2,0);
	} // y = 0 linje | null-linje

	if (e2d.ucX1 < 0 && e2d.ucX2 > 0){
		e2d.moveTo(0,e2d.ucY1);
		e2d.lineTo(0,e2d.ucY2);
	}
	
	e2d.stroke();
}

// For kompatibilitet: Setter window og viewport
function tegnKoordinatsystem(x1,x2,y1,y2,farge="grey",tittel="f(x)",desimalX=2,desimalY=2,
								xtittel="x-akse",ytittel="y-akse"){
	var umc=[],ncc=[],tekster=[];
	umc[0]=x1; 	umc[1]=x2; umc[2]=y1; umc[3]= y2;
	ncc[0]=0.; 	ncc[1]=1.; ncc[2]=0.1; ncc[3]= 0.8;

	tekster[0] = tittel;
	tekster[1] = xtittel;
	tekster[2] = ytittel;
	e2d.clearCanvas();
	tegnAkserUMC(umc,ncc,tekster,desimalX,desimalY);
}

function tegnAkserUMC(umc,ncc,tekster,desimalX=2,desimalY=2,viskut=true){
// Definerer koordinattransformasjoner
    if (umc.length < 4 || ncc.length < 4 || tekster.length < 3 ){
		console.log("tegnUMCAkser--> Feil arraydata !");
	}
	e2d.xRange(umc[0],umc[1]); 	// 1.aksens begrensninger
	e2d.yRange(umc[2],umc[3]); 	// 2.aksens begrensninger
	e2d.viewport(ncc[0],ncc[1],ncc[2],ncc[3]);
	if (viskut) e2d.clearCanvas();
	e2d.drawBoundary();
	tegnAkserXY(tekster[0],tekster[1],tekster[2],desimalX,desimalY);
}

function finnPentIntervall(verdi1,verdi2){
	var eksponent, pentTall, antall;
	var faktor = [2,2.5,5,7.5];
	eksponent = Math.round(Math.log10(verdi2-verdi1));
	penAvstand = Math.pow(10,eksponent-1);

	antall = Math.ceil((verdi2-verdi1)/penAvstand);
	indeks 	= -1;
	while (antall > 10 ){
		indeks = indeks + 1;
		antall = Math.ceil( (verdi2-verdi1)/(penAvstand*faktor[indeks]));
	}
	if (indeks !== -1) penAvstand = penAvstand*faktor[indeks] ;

	var penV1,penV2;
	penV1 = (Math.round ((verdi1-0.1*penAvstand)/penAvstand))*penAvstand;
	penV2 = (Math.round ((verdi2+0.1*penAvstand)/penAvstand))*penAvstand;

	return [penV1,penV2,penAvstand];
}

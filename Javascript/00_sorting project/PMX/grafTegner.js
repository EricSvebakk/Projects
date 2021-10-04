/*
	Formål:
		Verktøykasse for grafisk presentasjon i forbindelse med funksjonsdrøfting i
		matematikkundervisningen ved VGS.

	Dette kodebiblioteket forutsetter at tegningen foregår i et easy2DGraphics objekt
    med navn e2d (Global variabel).

	Biblioteker som er benyttet:
		* easy2DGraphics
		* numeriskeMetoder

	Funksjoner i dette kodebiblioteket:
		* definere og tegne koordinatsystem
		* tegne grafen til en funksjon i et definert koordinatsystem
		* tegne punkter på grafen til en funksjon

	FORUTSETNINGER:
		* Her antas at det i noen tilfeller at det finnes en JS-funktion på formen:
		  function matFunksjon(x){
			return y = <uttrykk>;
		  }
		* Global variabel e2d eksisterer for easy2DGraphics grafikkbiblioteket.


    FRI INTERN BRUK PÅ FAGERLIA VGS,ÅLESUND (Rolf Magne Aasen)
	8.januar 2019
*/

function tegnGrafFunksjon(matFunksjon,x1,x2,farge="red",antallPunkt=200){
	var x = [], y = [];
	var xtemp;
	for (var i =0 ; i < antallPunkt ; i++){
		xtemp = x1 + i*(x2-x1)/(antallPunkt-1);
		y[i] = matFunksjon(xtemp);
		x[i] = xtemp;
	}
	e2d.polyLine(x,y,farge);
}

function tegnTangent(matFunksjon,x,desimaler=3,farge="green"){
	var stigning = deriverNumerisk(matFunksjon,x);
	var y = matFunksjon(x);
	var x1,y1, x2,y2; // Skal være to endepunkter på tangentens linjestykke
	var xdiff = (e2d.ucX2-e2d.ucX1)/5.;   // Andel av x-range

	x1 = x - (0.5*xdiff);
	x2 = x + (0.5*xdiff);
	y1 = y-stigning*(0.5*xdiff);
	y2 = y+stigning*(0.5*xdiff);

	e2d.beginPath();
	e2d.context.strokeStyle = farge;
	e2d.moveTo(x1,y1);
	e2d.lineTo(x2,y2);
	e2d.stroke();
	if (desimaler > 0 ){
	e2d.text(x,y,"   a="+stigning.toFixed(desimaler),"red","12px Arial","left","center");
	}
}

function tegnGrafPunkter(matFunksjon,xArray,punkttype="cross",farge="red"){
	var yArray = [];
	for (var i =0 ; i < xArray.length ; i++){
		yArray[i] = matFunksjon(xArray[i]);
	}
	e2d.polyMarker(xArray,yArray,punkttype,farge);
}
function tegnGrafDerivert(matFunksjon,x1,x2,farge="brown",antallPunkt=200){
	var xArray = [], yArray=[];
	var xstep;

	xstep = (x2-x1)/(antallPunkt-1);
	for (var i=0; i<=antallPunkt;i++){
		x = x1 + i*xstep;
		xArray[i] = x;
		yArray[i] = deriverFunksjon(matFunksjon,x);
	}
	e2d.polyLine(xArray,yArray,farge);
}

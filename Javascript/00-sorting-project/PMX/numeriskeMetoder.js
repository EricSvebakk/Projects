/*
	Formål:
		Verktøykasse for numerisk løsning av matematiske problemstillinger.
		Relevant for matematikkundervisningen ved VGS.

	Biblioteker som er benyttet: Ingen

	Numeriske løsninger i dette biblioteket for beregning av:
		* verdimengde
		* vekstfart
		* derivert (momentan vekstfart)
		* nullpunkter
		* løse ligning
		* skjæring mellom funksjoner

	FORUTSETNINGER:
		* Her antas at det i noen tilfeller at det finnes en JS-funktion på formen:
		  function matFunksjon(x){
			return y = <uttrykk>;
		  }
		* Global variabel e2d eksisterer for easy2DGraphics grafikkbiblioteket.
	}

    FRI INTERN BRUK PÅ FAGERLIA VGS,ÅLESUND (Rolf Magne Aasen)
	8.januar 2019
*/

/*----------------------------------------------------------------------------------------------
	Formål: Finne verdimengden til en matematisk funksjon definert som en JS-function

	Metode: For-løkke over et gitt antall punkter i et spesifisert x-intervall.
			Punktenes beregnede y-verdier benyttes til å finne tilnærmede verdier for
			verdimengden.
	Input:
		xstart,xslutt		   	- Begrensning av x-området
		antallPunkt	(valgfri)	- Antall punkter benytter ved bestemmelse av verdimengden.
	Return:
		verdimengde				- Array med de to verdiene
								  Posisjon 0: lav verdi, Posisjon 1: høy verdi
----------------------------------------------------------------------------------------------*/
function verdimengdeFunksjon(matFunksjon,xstart,xslutt,antallPunkt=1000){
	var resultat = [];
	var ylow  = matFunksjon(xstart);
	var yhigh = matFunksjon(xstart);
	var xinc  = (xslutt - xstart)/(antallPunkt-1);
	for (var x = xstart; x<=xslutt; x = x+xinc){
		if (ylow > matFunksjon(x) ) ylow = matFunksjon(x);
		if (yhigh< matFunksjon(x) ) yhigh = matFunksjon(x);
	}
	resultat[0] = ylow;
	resultat[1] = yhigh;
	return resultat;
}
/*----------------------------------------------------------------------------------------------
	Formål: Finne den deriverte til en matematisk funksjon definert som en JS-function

	Metode: Beregner y-verdiene til to nabopunkter av den oppgitte x-verdien. Avstanden (langs x) mellom
			nabopunktene er gitt som et valgfritt argument.
	Input:
		matFunksjon			- Den matematiske funksjonen gitt som en JS-function
		x		   			- x-verdien som skal benyttes i beregningen
		deltaX	(valgfri)	- Avstanden (i x ) mellom nabopunktene ved beregning av stigningstallet
	Return:
		derivert			- Den deriverte i det angitte punktet
----------------------------------------------------------------------------------------------*/
function deriverFunksjon(matFunksjon,x,deltaX=0.00001){
	var derivert;
	derivert = (  matFunksjon(x+0.5*deltaX)-matFunksjon(x-0.5*deltaX)) / deltaX;
	return derivert;
}
function deriverNumerisk(matFunksjon,x,deltaX=0.00001){ // For kompatibilitet
	return deriverFunksjon(matFunksjon,x,deltaX=0.00001);
}
/*----------------------------------------------------------------------------------------------
	Formål: Finne vekstfarten til en matematisk funksjon definert som en JS-function

	Metode: Beregner y-verdiene til to argumenter med x-verdier.
	Input:
		matFunksjon			- Den matematiske funksjonen gitt som en JS-function
		x1,x2		   		- x-verdiene til punkt 1 og punkt 2 i beregningen
	Return:
		vekstfart			- Den beregnede vekstfarten

----------------------------------------------------------------------------------------------*/
function vekstfartFunksjon(matFunksjon,x1,x2){
	var vekstfart;
	y1 = matFunksjon(x1);
	y2 = matFunksjon(x2);
	vekstfart = (y2-y1)/(x2-x1);
	return vekstfart;
}
/*----------------------------------------------------------------------------------------------
	Formål: finne alle nullpunktene til et funksjonsuttrykk

	Metode: For-løkke over x-intervall. Skjæring i det intervallet der produktet av
			y-verdiene til to nabopunkt er negativt.
			Løsning defineres numerisk som midpunktet. Presisjon i svaret avhengig av
			argumentet deltaX (metode kan raffineres for viderekommende, feks. ved halveringsmetoden)

	Input:
		xstart,xslutt		   - Begrensning av x-området som løsningen skal finnes innenfor
		deltaX	(valgfri)	   - deltaX gir avstanden mellom punktene

	Return:
		listeNullpunkt		   - Array med nullpunkter (lengde=0 betyr ingen nullpunkt funnet)
----------------------------------------------------------------------------------------------*/
function nullpunktFunksjon(funksjon,xstart,xslutt,antallIntervall=1000){
	var xinc = (x2-x1)/antallIntervall;
	var antallNullpunkt = 0;
	var listeNullpunkt = [];
	var yn,ym;
	var eps = 0.0000001; // Bruker denne for å sjekke likhet mellom desimaltall
	var x1=xstart, x2=xslutt;
	for (var x=x1; x<x2; x = x+xinc){
		yn = funksjon(x);
		ym = funksjon(x+xinc);
		if (yn*ym <= 0) {
			if (yn*ym < 0) {
				antallNullpunkt = antallNullpunkt+1;
				listeNullpunkt[antallNullpunkt-1] = (x+x+xinc)/2.; // Bruker midtpunktet
			}
			else if (Math.abs(yn) < eps){		// Nullpunktet er i x !
				antallNullpunkt = antallNullpunkt+1;
				listeNullpunkt[antallNullpunkt-1] = x;
			}
			else if (Math.abs(ym) < eps){		// Nullpunktet er for x+xinc !
				antallNullpunkt = antallNullpunkt+1;
				listeNullpunkt[antallNullpunkt-1] = x+xinc; // Algoritmen kan forbedres
			}
		}
		// Fjern eventuelt doble nullpunkt (kan forekomme hvis ym er nullpunkt)
		if (antallNullpunkt >= 2 && Math.abs(listeNullpunkt[antallNullpunkt-1] - listeNullpunkt[antallNullpunkt-2])<eps){
			antallNullpunkt = antallNullpunkt - 1;
		}
	}
	return listeNullpunkt;
}
/*----------------------------------------------------------------------------------------------
	Formål: løse en ligning der HS og VS er gitt ved hver sin JS-function.

	Metode: For-løkke over x-intervall. Skjæring i det intervallet der produktet av
			y-differensen (mellom de to funksjonene) er negativt.
			Løsning defineres numerisk som midpunktet. Presisjon i svaret avhengig av
			argumentet deltaX (metode kan raffineres for viderekommende ved haveringsmetoden eller
			lignende)

	Input:
		venstreSide, høyreSide - JS-function som beskriver venstre og høyre side i uttrykket
		xstart,xslutt		   - Begrensning av x-området som løsningen skal finnes innenfor
		deltaX	(valgfri)	   - deltaX gir avstanden mellom punktene
	Return:
		xArray				   - En array/liste med funnede x-verdier.
								 En tom liste betyr at ingen verdier er funnet.
----------------------------------------------------------------------------------------------*/
function løsLigning(venstreSide,høyreSide,xstart,xslutt,deltaX=0.0001){
		var xArray = [];
		var ydiffSist,ydiff;
	ydiffSist = høyreSide(xstart)-venstreSide(xstart);
//	deltaX = (xslutt-xstart)/antallIntervall;
	for (var x=xstart+deltaX; x<=xslutt; x=x+deltaX){
		ydiff = høyreSide(x)- venstreSide(x);
		if (ydiff * ydiffSist <= 0 ){ // Har krysset hverandre. Fø
			xArray.push(x-0.5*deltaX);
		}
		ydiffSist = ydiff;
	}
	return xArray;
}
/*----------------------------------------------------------------------------------------------
	Formål: finne skjæring mellom to funksjoner gitt ved en JS function

	Metode: For-løkke over x-intervall. Skjæring i det intervallet der produktet av
			y-differensen (mellom de to funksjonene) er negativt.
			Løsning defineres numerisk som midpunktet. Presisjon i svaret avhengig av
			argumentet antallIntervall (metode kan raffineres for viderekommende)

	Input:
		matFunksjon1, matFunksjon2 	- JS-function som beskriver venstre og høyre side i uttrykket
		xstart,xslutt		   		- Begrensning av x-området som løsningen skal finnes innenfor
		antallIntervall	(valgfri)	- deltaX gir avstanden mellom punktene

----------------------------------------------------------------------------------------------*/
function skjæringFunksjoner(matFunksjon1,matFunksjon2,xstart,xslutt,antallIntervall=1000){
	return løsLigning(matFunksjon1,matFunksjon2,xstart,xslutt,(xslutt-xstart)/antallIntervall);
}

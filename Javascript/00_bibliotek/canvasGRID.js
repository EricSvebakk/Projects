
/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
class canvasGRID {
	constructor(canvasID = "canvas", bredde = 600, høyde = 600, gridLayout = true, x1 = 0, y1 = 0, x2 = 10, y2 = 10, margin = 10) {
		
		// Oversetter canvas fra pixelkoordinater til verdenskoordinater
		this.gridLayout = gridLayout;

		// Lager en container til canvas i HTML
		let div = document.createElement("div");
		div.id = canvasID + "_div";
		div.style.float = "left";
		document.body.appendChild(div);

		// Lager canvas i HTML
		let canvas = document.createElement("canvas");
		canvas.id = canvasID;
		canvas.width = bredde * 2;
		canvas.height = høyde * 2;
		canvas.style.width = bredde + "px";
		canvas.style.height = høyde + "px";
		canvas.style.cursor = "crosshair";
		canvas.style.background = "white";
		canvas.style.margin = margin + "px";
		$(div.id).appendChild(canvas);

		// x og y verdier
		this.x1 = x1;
		this.x2 = x2;
		this.y1 = y1;
		this.y2 = y2;

		// canvas tilkobling
		this.cnv = $(canvasID);
		this.ctx = this.cnv.getContext("2d");

		// canvas verdier
		this.cs = 24;
		this.cx = this.cnv.width;
		this.cy = this.cnv.height;
		this.csx = this.cx / this.cs;
		this.csy = this.cy / this.cs;
		this.margin = margin;

		// normalized canvas coordinates
		this.ncc = [];
		this.ncc[0] = this.csx;
		this.ncc[1] = this.cx - this.csx;
		this.ncc[2] = this.csy;
		this.ncc[3] = this.cy - this.csy;

		// Beregner avstanden mellom x- og y-verdier
		if (this.gridLayout) {
			this.deltaX = (this.ncc[1] - this.ncc[0]) / (this.x2 - this.x1);
			this.deltaY = (this.ncc[3] - this.ncc[2]) / (this.y2 - this.y1);
		} else {
			this.deltaX = this.x2 - this.x1;
			this.deltaY = this.y2 - this.y1;
		}

		this.blankCanvas("white");
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	pixelOversetter(inputArray = [], pad = true, poly = 0) {
		const oversatt = [];

		let transX = x => this.deltaX * x,
			transY = y => this.deltaY * y;

		let transPadX = x => this.csx + this.deltaX * x - this.deltaX * this.x1,
			transPadY = y => this.cy - (this.csy + this.deltaY * y - this.deltaY * this.y1);

		if (poly == 0) {
			for (let i = 0; i < inputArray.length; i++) {
				if (pad) {
					if (i % 2 == 0) oversatt[i] = transPadX(inputArray[i]);
					if (i % 2 == 1) oversatt[i] = transPadY(inputArray[i]);
				} else {
					if (i % 2 == 0) oversatt[i] = transX(inputArray[i]);
					if (i % 2 == 1) oversatt[i] = transY(inputArray[i]);
				}
			}
		} else {
			for (let i = 0; i < inputArray.length; i++) {
				if (poly == "x") oversatt[i] = transPadX(inputArray[i]);
				if (poly == "y") oversatt[i] = transPadY(inputArray[i]);
			}
		}
		return oversatt;
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	start(x, y, oversatt = true) {
		this.ctx.beginPath();

		if (this.gridLayout && oversatt) {
			let nyXY = this.pixelOversetter([x, y], true);
			x = nyXY[0];
			y = nyXY[1];
		}

		this.ctx.moveTo(x, y);
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	linje(x, y, farge, bredde = 1, stiplet = false, oversatt = true) {
		this.ctx.strokeStyle = farge;
		this.ctx.fillStyle = farge;
		this.ctx.lineWidth = bredde;

		if (this.gridLayout && oversatt) {
			let nyXY = this.pixelOversetter([x, y], true);
			x = nyXY[0];
			y = nyXY[1];
		}

		if (stiplet) this.ctx.setLineDash([3, 4]);
		else this.ctx.setLineDash([0, 0]);

		this.ctx.lineTo(x, y);
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	linjestykke(x1, y1, x2, y2, farge, bredde = 5, stiplet = false) {
		this.ctx.lineWidth = bredde;

		this.start(x1, y1);
		this.linje(x2, y2, farge, stiplet);
		this.stopp();
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	stopp(fyll = false) {
		if (fyll) this.ctx.fill();
		else this.ctx.stroke();
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	firkant(x1, y1, x2, y2, farge, fyll = true, info = false, bredde = 1) {
		
		this.start(x1, y1);
		this.linje(x2, y1, farge, bredde);
		this.linje(x2, y2, farge, bredde);
		this.linje(x1, y2, farge, bredde);
		this.linje(x1, y1, farge, bredde);
		this.stopp(fyll);

		/* if (info) {
			let avgX = (parseInt(x1, 10) + parseInt(x2, 10)) / 2;
			let avgY = (parseInt(y1, 10) + parseInt(y2, 10)) / 2;
			let deltaX = (parseInt(x2, 10) - parseInt(x1, 10));
			let deltaY = (parseInt(y2, 10) - parseInt(y1, 10));
			this.tekst(avgX, avgY, "B=" + deltaX, "black", "30px Arial", 0, 0, 20);
			this.tekst(avgX, avgY, "H=" + deltaY, "black", "", 0, 0, -20);
		} */

		if (info) {
			let avgX = (parseInt(x1, 10) + parseInt(x2, 10)) / 2;
			let avgY = (parseInt(y1, 10) + parseInt(y2, 10)) / 2;
			let deltaX = (parseInt(x2, 10) - parseInt(x1, 10));
			let deltaY = (parseInt(y2, 10) - parseInt(y1, 10));
			this.tekst(avgX, y1, "B=" + deltaX, "black", "30px Arial", 0, 0, 30);
			this.tekst(x2, avgY, "H=" + deltaY, "black", "", 0, 40, 0);
			this.tekst(avgX, avgY, deltaX + ":" + deltaY, "black", "", 0, 0, 0);
		}
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	sirkel(x, y, rx, ry, farge = "red", fyll = true, info = false) {

		this.ctx.fillStyle = farge;
		this.ctx.strokeStyle = farge;
		this.ctx.lineWidth = 2;
		this.ctx.setLineDash([0, 0]);

		this.xS = x;
		this.yS = y;

		for (let i = 0; i < 2 * Math.PI; i += 0.001) {
    		this.xS = x - rx * Math.cos(i);
			this.yS = y - ry * Math.sin(i);
			if (i == 0) this.start(this.xS, this.yS);
			else this.linje(this.xS, this.yS, farge);
		}
		this.stopp(fyll);

		if (info) {
			if (rx == ry) {
				this.tekst(x, y, "S=(" + x + "," + y + ")", "black", "", 0, 0, 5);
				this.tekst(x, y, "R=" + rx, "black", "", 0, 0, -5);
			} else {
				this.tekst(x, y, "S=(" + x + "," + y + ")", "black", "", 0, 0, 10);
				this.tekst(x, y, "rX=" + rx, "black", "", 0, 0, 0);
				this.tekst(x, y, "rY=" + ry, "black", "", 0, 0, -10);
			}
		}
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	figur(xArray, yArray, farge="red",fyll=true) {
		this.ctx.fillStyle = farge;
		this.ctx.strokeStyle = farge;
		this.ctx.lineWidth = 2;

		this.start(xArray[0],yArray[0]);

		for (let i = 0; i < xArray.length; i++) {
			this.linje(xArray[i], yArray[i], farge);
		}
		this.linje(xArray[0],yArray[0]);
		this.stopp(fyll);
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	tekst(x, y, tekst, farge = "black", font = "30px Arial", rotasjon = 0, offsetX = 0, offsetY = 0) {
		this.ctx.textBaseline = "middle";
		this.ctx.textAlign = "center";
		this.ctx.font = font;
		this.ctx.fillStyle = farge;

		if (this.gridLayout) {
			let nyXY = this.pixelOversetter([x, y], true);
			x = nyXY[0];
			y = nyXY[1];
		}

		this.ctx.translate(x, y);
		this.ctx.rotate(rotasjon);
		this.ctx.fillText(tekst, offsetX, offsetY);
		this.ctx.rotate(rotasjon * -1);
		this.ctx.translate(x * -1, y * -1);
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	oppdaterCanvas(nyX1,nyY1, nyX2, nyY2) {
		this.x1 = nyX1;
		this.y1 = nyY1;
		this.x2 = nyX2;
		this.y2 = nyY2;
		this.blankCanvas()
		this.grid();
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	blankCanvas(farge="white") {
		this.ctx.beginPath();
		this.ctx.fillStyle = farge;
		this.ctx.fillRect(0, 0, this.cx, this.cy);
		this.ctx.fill();
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	grid(tekst=true,kunRute=true) {
		this.ctx.lineWidth = 1;
		this.ctx.textBaseline = "middle";
		this.ctx.textAlign = "center";

		/* this.firkant(this.csx*-1,	this.csy*-1,	this.x1,			this.y2+this.csy,	"white");
		this.firkant(this.x2,		this.csy*-1,	this.x2+this.csx,	this.y2+this.csy,	"white");
		this.firkant(this.csx*-1,	this.csy*-1,	this.x2+this.csx,	this.y1,			"white");
		this.firkant(this.csx*-1,	this.y2+0.02,	this.x2+this.csx,	this.y2+this.csy, 	"white"); */

		this.firkant(this.x1, this.y1, this.x2, this.y2, "black", false);

		let gridX = this.intervall(this.x1, this.x2),
			gridY = this.intervall(this.y1, this.y2);

		// tegn loddrette gridstreker
		if (kunRute) {
			for (let i = gridX[0]; i <= gridX[1]; i += gridX[2]) {
				if (i >= this.x1 && i <= this.x2) {
					this.start(i, this.y1);
					this.linje(i, this.y2, "#aaa", 1, true);
					this.stopp();

					if (tekst) {
						this.tekst(i, this.y1, i.toFixed(1), "black", "20px Arial", 0, 0, 20);
						this.tekst(i, this.y2, i.toFixed(1), "black", "", 0, 0, -20);
					}
				}
			}

			// tegn vannrette gridestreker
			for (let i = gridY[0]; i <= gridY[1]; i += gridY[2]) {
				if (i >= this.y1 && i <= this.y2) {
					this.start(this.x1, i);
					this.linje(this.x2, i, "#aaa", 1, true);
					this.stopp();

					if (tekst) {
						this.tekst(this.x1, i, i.toFixed(1), "black", "", 0, -20, 0);
						this.tekst(this.x2, i, i.toFixed(1), "black", "", 0, 20, 0);
					}
				}
			}
		}
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	intervall(verdi1, verdi2) {

		var eksponent = Math.round(Math.log10(verdi2 - verdi1)),
			faktor = [2, 2.5, 5, 7.5],
			penAvstand = Math.pow(10, eksponent - 1),
			antall = Math.ceil((verdi2 - verdi1) / penAvstand),
			indeks = -1;

		while (antall > 10) {
			indeks += 1;
			antall = Math.ceil((verdi2 - verdi1) / (penAvstand * faktor[indeks]));
		}

		if (indeks !== -1) penAvstand = penAvstand * faktor[indeks];

		var penV1 = (Math.round((verdi1 - 0.1 * penAvstand) / penAvstand)) * penAvstand,
			penV2 = (Math.round((verdi2 + 0.1 * penAvstand) / penAvstand)) * penAvstand;

		return [penV1, penV2, penAvstand];
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
 	funksjon(funk, farge = "red") {
	 	let x = [],
			y = [],
			xtemp = 0,
			antallPunkt = 200;

		const deltaX = (j) => this.x1 + (j * (this.x2 - this.x1)) / antallPunkt;

		for (let j = 0; j < antallPunkt; j++) {
			xtemp = deltaX(j);
			if (funk(xtemp) > this.y1 && funk(xtemp) < this.y2) y[j] = funk(xtemp);
			x[j] = xtemp;
			
			for (let i in x) {
				if (i == 0) this.start(x[0], y[0]);
				else this.linje(x[i], y[i], farge);
			}
		}
		this.stopp();		  
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	mus(farge, hardlinje = true, trekanter = false) {
		let mousePressX = 0,
			mousePressY = 0,
			currentMouseX = 0,
			currentMouseY = 0,
			avrunding = 1;

		// Rare trekanter
		if (trekanter) {
			this.cnv.addEventListener("mousedown", (e) => {
				mousePressX = e.clientX - this.margin;
				mousePressY = e.clientY - this.margin;
				this.start(mousePressX, mousePressY, false);
				this.cnv.addEventListener("mouseup", () => {
					currentMouseX = e.clientX - this.margin;
					currentMouseY = e.clientY - this.margin;
					this.linje(currentMouseX, currentMouseY, farge, 1, false, false);
					this.stopp()
				});
			});
		}
		
		// muspeker linje er ikke rett
		else if (hardlinje) {
			this.cnv.addEventListener("mousedown", (e) => {
				mousePressX = e.clientX - this.margin;
				mousePressY = e.clientY - this.margin;
				this.start(mousePressX, mousePressY, false);
			});

			this.cnv.addEventListener("mouseup", (e) => {
				currentMouseX = e.clientX - this.margin;
				currentMouseY = e.clientY - this.margin;
				this.linje(currentMouseX, currentMouseY, farge, 1, false, false);
				this.stopp()
			});
		} 
		
		// muspeker linje er rett
		else if (!hardlinje) {
			this.cnv.addEventListener("mousedown", (e) => {
				mousePressX = e.clientX - this.margin;
				mousePressY = e.clientY - this.margin;
				this.start(mousePressX, mousePressY, false);

				this.cnv.addEventListener("mousemove", (e) => {
					currentMouseX = (Math.round((e.clientX - this.margin) / avrunding)) * avrunding;
					currentMouseY = (Math.round((e.clientY - this.margin) / avrunding)) * avrunding;
					this.linje(currentMouseX, currentMouseY, farge, 1, false, false);
				});
			});
			this.cnv.addEventListener("mouseup", () => this.stopp());
		}
	}

/*==========================================================================/
/---------------------------------------------------------------------------/
/==========================================================================*/
	/* barGraph(x1, y1, x2, y2, data, levels=1, consoleData = false) {

		let dataKeys = Object.keys(data),
			dataValues = Object.values(data),
			largestValue = 1,
			segmentX = (x2-x1) / (dataValues.length),
			segmentY = undefined,
			offsetY = this.cy / 40,
			twoLayers = true;

			console.log(dataValues);

		// Graf beregninger
		let graphX1 = (input) => (x1 + input * segmentX),
			graphX2 = (input) => (x1 + input * segmentX) + segmentX,
			graphY2 = (input, divisor) => y1 + ((input / divisor) * segmentY),
			txtKeyX1 = (input) => (x1 + input * segmentX) + (segmentX / 2);
			//txtVal1Y = (input, divisor) => y1 + ((input / divisor) * segmentY),
			//txtVal2Y = (input, divisor) => y1 + ((input / divisor) * segmentY);

		let graph2X1 = (input1, input2) => (x1 + (input1 * segmentX) + (input2 * (segmentX / 3))),
			graph2X2 = (input1, input2) => (x1 + (input1 * segmentX) + (input2 * (segmentX / 3))) + (segmentX / 3),
			txtKey2X1 = (input1, input2) => (x1 + (input1 * segmentX) + (input2 * (segmentX / 3))) + (segmentX / 6),
			graph2Y2 = (input1, input2, divisor) => y1 + 1 + ((Object.values(input1)[input2] / divisor) * segmentY);

		let keyLength = (input) => Object.keys(input).length,
			key = (input) => Object.keys(input);

		//let nyGraphX1 = (input = []) => ()

		// Finner største verdi
		for (let i in dataValues) {
			console.log("yet:", keyLength(dataValues[i]))
			if (keyLength(dataValues[i]) > 0) {

				

				twoLayers = true;
				segmentY = (y2 - y1 - 1);
				segmentX = (y2 - y1);

				for (let j in Object.keys(dataValues[i])) {
					if (Math.abs(Object.values(dataValues[i])[j]) > Math.abs(largestValue)) largestValue = Object.values(dataValues[i])[j];
				}
			} else {
				segmentY = (y2 - y1);
				if (Math.abs(dataValues[i]) > Math.abs(largestValue)) largestValue = dataValues[i];
			}		
		}	


		
		// Tegner bakgrunn
		if (twoLayers) {
			this.firkant(x1, y1+1, x2, y2, "lightgrey");
			this.firkant(x1, y1+1, x2, y2, "black", false);
		} else {
			this.firkant(x1, y1, x2, y2, "lightgrey");
			this.firkant(x1, y1, x2, y2, "black", false);
		}

		// Tegner stolper som viser størrelsene av verdier fra data.
		for (let i in dataValues) {

			if (keyLength) {

				for (let j in key(dataValues[i])) {
					//console.log(data[Object.keys(data)[i]]);
					this.firkant(graph2X1(i, j), y1 + 1, graph2X2(i, j), graph2Y2(dataValues[i], j, largestValue), randomColour(1));
					this.firkant(graph2X1(i, j), y1 + 1, graph2X2(i, j), graph2Y2(dataValues[i], j, largestValue), "black", false);
					this.tekst(txtKey2X1(i, j), y1 + 1, Object.keys(dataValues[i])[j], "black", "20px Arial", 0, 0, offsetY);

					if (Object.values(dataValues[i])[j] > largestValue / 5) {
						this.tekst(txtKey2X1(i, j), graph2Y2(dataValues[i], j, largestValue), Object.values(dataValues[i])[j], "black", "20px Arial", 0, 0, offsetY);
					} else {
						this.tekst(txtKey2X1(i, j), graph2Y2(dataValues[i], j, largestValue), Object.values(dataValues[i])[j], "black", "20px Arial", 0, 0, -offsetY);
					}
				}
				this.tekst(txtKeyX1(i), y1, Object.keys(data)[i], "black", "20px Arial", 0, 0, -offsetY);
				this.firkant(graphX1(i), y1, graphX2(i), y1 + 1, "black", false);
				this.firkant(graphX1(i), y1, graphX2(i), y1 + 0.5, "black", false);




			} else {
				
				this.firkant(graphX1(i), y1, graphX2(i), graphY2(dataValues[i], largestValue), randomColour(1));
				this.firkant(graphX1(i), y1, graphX2(i), graphY2(dataValues[i], largestValue), "black", false);
				this.tekst(txtKeyX1(i), y1, dataKeys[i], "black", "20px Arial", 0, 0, offsetY);

				if (dataValues[i] > largestValue / 5) {
					this.tekst(txtKeyX1(i), txtVal1Y(dataValues[i], largestValue), dataValues[i].toFixed(1), "black", "20px Arial", 0, 0, offsetY);
				} else {
					this.tekst(txtKeyX1(i), txtVal2Y(dataValues[i], largestValue), dataValues[i].toFixed(1), "black", "20px Arial", 0, 0, -offsetY);
				}
			}
		}

		// printing av data
		if (consoleData) {
			for (let i in dataValues) console.log(dataKeys[i], ":", dataValues[i]);
		}

	} */








	barGraph(x1, y1, x2, y2, data, ratio = 0.2, font = "15px Arial", consoleData = false) {

		let opl = objectsPerLevel(data),
			largestY = largestValue(data),
			layers = opl.length - 1,
			offsetY = this.cy / 40,
			levels = [],
			level = -1;

		let segmentY = (y2 - y1 - layers), 
			deltaX = x2 - x1,
			deltaY = y2 - y1;

		let boxX1 = (input) => x1 + (levels[input] * (deltaX / opl[input])),
			boxX2 = (input) => x1 + (levels[input] * (deltaX / opl[input])) + (deltaX / opl[input]),
			boxY  = (input) => y1 + (((input / (layers+1)) * deltaY) * ratio),
			barY2 = (input) => y1 + layers + ((input / largestY) * segmentY),
			textX = (input) => x1 + (levels[input] * (deltaX / opl[input])) + ((deltaX / opl[input]) / 2),
			textY = (input) => y1 + (((input / (layers + 1)) * deltaY) * ratio) + ((((1 / (layers + 1)) * deltaY) * ratio) / 2);

		// Tegner bakgrunn
		this.firkant(x1, y1, x2, y2, "lightgrey");
		this.firkant(x1, y1, x2, y2, "black", false);

		iterator(data);
		function iterator(obj) {
			level++;
			Object.keys(obj).forEach(key => {
				if (typeof levels[level] === 'undefined') levels[level] = 0;

				tegn.firkant(boxX1(level), boxY(level), boxX2(level), boxY(level + 1), "darkgrey");
				tegn.firkant(boxX1(level), boxY(level), boxX2(level), boxY(level + 1), "black", false);
				tegn.tekst(textX(level), textY(level), key, "black", font, (level * -30) * Math.PI / 180);

				if (level == layers) {
					tegn.firkant(boxX1(level), boxY(level + 1), boxX2(level), barY2(obj[key]), randomColour(1));
					tegn.firkant(boxX1(level), boxY(level + 1), boxX2(level), barY2(obj[key]), "black", false);
					console.log(barY2(obj[key]));

					if (Math.abs(obj[key]) > Math.abs(largestY / 5)) {
						tegn.tekst(textX(level), barY2(obj[key]), obj[key].toFixed(1), "black", font, 0, 0, offsetY);
					} else {
						tegn.tekst(textX(level), barY2(obj[key]), obj[key].toFixed(1), "black", font, 0, 0, -offsetY);
					}

					if (consoleData) console.log(key, obj[key]);
				}
				
				/* console.log("")
				console.log("lvl:", level);
				console.log("key:", key);
				console.log("X:", boxX1(levels[level], opl[level]).toFixed(2), boxX2(levels[level], opl[level]).toFixed(2))
				console.log("Y:", boxY(level).toFixed(2), boxY(level + 1).toFixed(2));
				console.log("tY:", textY(level).toFixed(2));
				console.log("boxY:", level, layers, deltaY, ratio);
				console.log("f:", y1+"+((("+level+"/"+layers+")"+"*"+deltaY+")*"+ratio+")=", y1+(((level/layers)*deltaY)*ratio)); */

				levels[level]++;
				iterator(obj[key]);
			})
			level--;
		}

		// printing av data
		if (consoleData) {
			console.log("");
			/* for (let i in dataValues) console.log(dataKeys[i], ":", dataValues[i]); */

			console.log("opl:", opl);
			console.log("data:", data);
			console.log("largest:", largestY);
			console.log("layers:", layers);
			console.log("deltaX:", deltaX);
			console.log("deltaY:", deltaY);
		}
	}

	// class end
}


class cavarty extends canvasGRID{
	constructor(){
		super();
	}
}

class creola extends cavarty{
	constructor(){
		super();
	}
}

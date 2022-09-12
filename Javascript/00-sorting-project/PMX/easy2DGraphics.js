/*
easy2DGraphis - a subset of the easy23DGraphics library.
Developed by Rolf Magne Aasen for educational purposes at Fagerlia VGS Ålesund.
Please read the user documentation to learn how to get started.
*/
class easy2DGraphics{  
	constructor(){ 								 
		this.version= "ver:7.jan.2019",
		this.canvas= "undefined", this.context= "undefined",
		this.backgroundColor="white",
		this.xScale = 200,this.yScale= 200,
		this.xMargin=  50,this.yMargin= 50,
		this.ncX1=  0.0, this.ncX2=  1.0, this.ncY1= 0.0, this.ncY2= 1.0,  // Normalised Canvas Coordinates
		this.ucX1=  0.0, this.ucX2= 10.0, this.ucY1= 0.0, this.ucY2= 10.0, // User Model Coordinates (unrotated)
		this.useMatrix=false;
		this.rotX=  0.0, this.rotY=  0.0, this.rotAngle=0.0,	    // Rotation point and rotation angle
		this.matrixA=1.0, this.matrixB=0.0,this.matrixC=0.0,        // x'=ax+by+c
		this.matrixD=0.0, this.matrixE=1.0,this.matrixF=0.0,	    // y'=dx+ey+f
		this.xLT=0.0, this.yLT=0.0,									// Last point
		this.colormap="red_blue",						  // When color is an integer (blue_red,red_blue)
		this.colValue1 = 0; this.colValue2 = 100;		  // Values to be used when mapping to a continous color scale
		this.print= false,								  // Set to true if you want to see details execution
		this.trace= false;										
	}
 
	init (canvas) { // Constructor for the program
		this.canvas = canvas;
		this.context = this.canvas.getContext("2d");	 
	}

	showData () { // For debuggin. Output to console
		console.log("-------------------------------------------------");
		console.log("E2D version:",this.version);
		console.log("Margins :",this.xMargin,this.yMargin);
		console.log("Viewport:",this.ncX1,this.ncX2,this.ncY1,this.ncY2);
		console.log("Window  :",this.ucX1,this.ucX2,this.ucY1,this.ucY2);
		console.log("-------------------------------------------------");
	} 
	//---
	//--- Section of functions related to mapping coordinates from a model coordinate system to
	//--- to the pixel coordinates used in the canvas. Rotation of the coordinate system is supported.
	//	
	margins(xMargin,yMargin){ // Set the canvas margin (give space for axes)
		this.xMargin = xMargin;
		this.yMargin = yMargin;
		
	} 

	window(xlow,xhigh,ylow,yhigh){ // Set x and y ranges for window transformations
		this.ucX1 = xlow;					 
		this.ucX2 = xhigh;	
		this.ucY1 = ylow;	
		this.ucY2 = yhigh;		
	} 

	xRange(xlow,xhigh,adjustInteger=false){ // Set x range only for window transformations
		this.ucX1 = xlow;	
		this.ucX2 = xhigh;	
		if (adjustInteger){
			this.ucX1 = Math.floor(xlow);	
			this.ucX2 = Math.ceil(xhigh);		
		}
	} 
 
	yRange(ylow,yhigh,adjustInteger=false){ // Set y range only for window transformations
		this.ucY1 = ylow;	
		this.ucY2 = yhigh;	
		if (adjustInteger){
			this.ucX1 = Math.floor(xlow);	
			this.ucX2 = Math.ceil(xhigh);		
		}
	} 
 
	viewport(xlow,xhigh,ylow,yhigh){ // Set x and y ranges for viewport transformations
		this.ncX1 = xlow;	
		this.ncX2 = xhigh;	
		this.ncY1 = ylow;	
		this.ncY2 = yhigh;
		this.xScale = (xhigh-xlow)*(this.canvas.width -2*this.xMargin);
		this.yScale = (yhigh-ylow)*(this.canvas.height-2*this.yMargin);
		
		if (this.print) console.log ("NDC " ,this.ncX1,this.ncX2,this.ncY1,this.ncY2 );
		if (this.print) console.log ("scaling " +this.xScale +" " +this.yScale );
		if (this.print) console.log ("margin " +this.xMargin +" " +this.yMargin);
	} 

	rotation(xRotation,yRotation,angle){ // Rotate relative to given rotation point
		this.rotX = xRotation; 
		this.rotY = yRotation;
		this.rotAngle = angle;  // Degrees
		this.useMatrix = true;
		
		var angleRad = (angle/180.)*Math.PI;
		var sinA = Math.sin(angleRad);
		var cosA = Math.cos(angleRad);
		
		this.matrixA =  cosA;
		this.matrixB = -1.*sinA;
		this.matrixC = -xRotation*cosA + yRotation*sinA + xRotation;
		this.matrixD =  sinA;
		this.matrixE =  cosA;
		this.matrixF = -xRotation*sinA - yRotation*cosA + yRotation;
		
		if (this.trace) console.log("Matrix: " +this.matrixA +" "+this.matrixB +" " +this.matrixC +" " );
		if (this.trace) console.log("        " +this.matrixD +" "+this.matrixE +" " +this.matrixF +" " );
	} 
	//	
	//--- Section of functions related to drawing of basic graphics primitives like:
	//--- lines,rectangles,markers,text.
	//
	/*--------------------------------------------------------------------------------
	Purpose: Clear the complete canvas area. 
			 Will use the color set by the backgroundColor attribute 
	----------------------------------------------------------------------------------*/	
	clearCanvas (){	// Clear the whole canvas with backgroundColor
		this.context.beginPath();
		this.context.fillStyle = this.backgroundColor;
		this.context.rect(0,0,this.canvas.width,this.canvas.height);
		this.context.fill();
	} 
	
	clearWindow (){	// Clear the window with backgroundColor
		this.fillRectangle(this.ucX1,this.ucY1,this.ucX2,this.ucY2,this.backgroundColor);
	}
	/*--------------------------------------------------------------------------------
	Purpose: Mark the start for a path to be drawn.
			 Call this method before moveTo and lineTo. Close the path by stroke() for
			 update in canvas.
	----------------------------------------------------------------------------------*/
	beginPath (){	// Start a path og line segments
		this.context.beginPath();
	} 
	/*--------------------------------------------------------------------------------
	Purpose: Close the path and draw as lines. Will be visible on html canvas
	----------------------------------------------------------------------------------*/
	stroke (){	// Close a path of line segments
		this.context.stroke();
	} 
	/*--------------------------------------------------------------------------------
	Purpose: Move the pen position to a given point. Defines a current position.
	Input
		x,y     	- 	arrays with x and y positions
	----------------------------------------------------------------------------------*/	
	moveTo(x,y) { // Move the pen (current position) to a starting point for line drawing (UMC)
		this.transformXY(x,y);
		this.context.moveTo(this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		if (this.trace) console.log ("moveTo  " +x +" " +y);
	} 
	/*--------------------------------------------------------------------------------
	Purpose: Draw a line from the current position to the input position.
			 Note that in order to get a visible result on the screen the path need
			 to be define. Use beginPath() in the start and stroke() in the end.
	Input
		x,y     	- 	arrays with x and y positions
	----------------------------------------------------------------------------------*/		
	lineTo(x,y) { // Draw a line segment from current position to a new position /current updated)
		this.transformXY(x,y);
		this.context.lineTo(this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		if (this.trace) console.log ("lineTo " +x +" " +y);
		
	} 
	/*--------------------------------------------------------------------------------
	Purpose: draw a line segments between a list of  points
			 a simple clipping approach is implemented.
	Input
		x,y     	- 	arrays with x and y positions
		color 		-	a web color name or a hue indeks [0,360]
		lineWidth 	-   defines the thickness of the line (1,2,..)
	----------------------------------------------------------------------------------*/		
	polyLine(x, y, color = "black", lineWidth = 1) { // Draw a polyline define by x any y arrays (UMC)
		var iL = -1, 
			iH = -1;

		for (i = 0; i < x.length; i++) {
			if (iL == -1 && x[i] >= this.ucX1) iL = i;
		}

		for (i = x.length - 1; i > iL; i--) {
			if (iH == -1 && x[i] <= this.ucX2) iH = i;
		}

		if (iL == -1) return;
		if (iH == -1) return

		// Above a simple clipping algoritm (do not plot outside x-range)
		this.context.beginPath();
		this.context.strokeStyle = color;
		this.context.lineWidth = lineWidth;
		for (var i = iL; i <= iH; i++) {
			if (i == iL)
				this.moveTo(x[i], y[i]);
			else
				this.lineTo(x[i], y[i]);
		}
		this.context.stroke();
	} 
	/*--------------------------------------------------------------------------------
	Purpose: draw a list of markers
	Input
		x,y     - 	arrays with x and y positions
		marker  -   type of marker (see marker method)
		color 	-	a web color name or a hue indeks [0,360]
	----------------------------------------------------------------------------------*/	
	polyMarker(x,y,marker="cross",color="black") { // Draw multiple markers in positions defined by x any y arrays (UMC)
		for (var i = 0; i < x.length ; i++ ) {
			if (x[i] >= this.ucX1 && x[i] <= this.ucX2) this.marker(x[i],y[i],marker,color);
		}
	} 
	/*--------------------------------------------------------------------------------
	Purpose: draw a filled area outlined by a polyline
	Input
		x,y     - 	arrays with x and y positions
		color 	-	a web color name or a hue indeks [0,360]
	----------------------------------------------------------------------------------*/	
	fillArea(x,y,color="red") { // Draw a polyline define by x any y arrays (UMC)
		this.context.beginPath();
		if (Number(color)){
			var colstring = 'hsl('+color.toFixed(0) +',100%,50%)';
			this.context.fillStyle = colstring;
		} else { 
			this.context.fillStyle = color;
		}
		for (var i = 0; i < x.length; i++ ) {
			if (i === 0 )this.moveTo(x[i],y[i]);
			else 		 this.lineTo(x[i],y[i]);
		}
		this.lineTo(x[0],y[0]);
		this.context.fill();
	} 
	polyFill(x,y,color="red") { // Draw a polyline define by x any y arrays (UMC)
		this.fillArea(x,y,xolor);
	}
	/*--------------------------------------------------------------------------------
	Purpose: draw a rectangle boundary
	Input
		x1,y1,x2,y2 - 	coordinates to two diagonal points in rectangle
		color 	 	-	a web color name or a hue indeks [0,360]
	----------------------------------------------------------------------------------*/		
	rectangle(x1,y1,x2,y2,color="black") { // Draw a border rectangle defined by two diagonal corners (UMC)
		this.beginPath();
		if (Number(color)){
			var colstring = 'hsl('+color.toFixed(0) +',100%,50%)';
			this.context.fillStyle = colstring;
		} else { 
			this.context.strokeStyle = color;
		}
		this.moveTo(x1,y1);
		this.lineTo(x2,y1);
		this.lineTo(x2,y2);
		this.lineTo(x1,y2);
		this.lineTo(x1,y1);
		this.stroke();
		if (this.trace) console.log ("rectangle B " +x1 +" " +y1 +" " + +x2 +" " +y2);

	} 
	/*--------------------------------------------------------------------------------
	Purpose: draw a filled rectangle
	Input
		x1,y1,x2,y2 - 	coordinates to two diagonal points in rectangle
		color 	 	-	a web color name or a hue indeks [0,360]
	----------------------------------------------------------------------------------*/	
	fillRectangle(x1,y1,x2,y2,color="blue") { // Draw a color filled rectangle  
		if (this.trace) console.log ("rectangle B " +x1 +" " +y1 +" " + +x2 +" " +y2);
		
		this.beginPath();
		this.moveTo(x1,y1);
		this.lineTo(x2,y1);
		this.lineTo(x2,y2);
		this.lineTo(x1,y2);
		this.lineTo(x1,y1);
		if (Number(color)){
			var colstring = 'hsl('+color.toFixed(0) +',100%,50%)';
			this.context.fillStyle = colstring;
		} else { 
			this.context.fillStyle = color;
		}
		this.context.fill();

	} 
	/*--------------------------------------------------------------------------------
	Purpose: draw a filled circle
	Input
		centerX,centerY 	- 	center of the circle
		radius				-   circle radius
		color (optional)  	-	a web color name or a hue indeks [0,360]
	----------------------------------------------------------------------------------*/	
	fillCircle(centerX,centerY,radius,color="yellow"){ // Draw a color filled circle
		this.context.beginPath();
		if (this.trace) console.log("fillCircle UC: ",centerX,centerY,radius);
		if (this.trace) console.log("fillCircle PX: " ,
								this.ucpxTransX(centerX),this.ucpxTransY(centerY), 
								this.ucpxTransX(radius)-this.ucpxTransX(0));
								
		this.context.arc(	this.ucpxTransX(centerX),this.ucpxTransY(centerY), 
								this.ucpxTransX(radius)-this.ucpxTransX(0), 0, 2 * Math.PI, false  );
		if (Number(color)){
			var colstring = 'hsl('+color.toFixed(0) +',100%,50%)';
			this.context.fillStyle = colstring;
		} else { 
			this.context.fillStyle = color;
		}						
		this.context.fillStyle = color;
		this.context.fill();
	} 
	/*-------------------------------------------------------------------------------------
	Purpose: draw a text
	Input
		x,y 	- 	text position
		text	-   text to draw
		color (optional)	 -	a web color name or a hue indeks [0,360]
		font  (optional)	 -  note the format like "10px Areal"
		align (optional)	 -  text position can be one of 
								left, right or center (strings - horizontal)
		baseline(optional)   -  text baseline can be one of
								top/bottom/middle/alphabetic/hanging (strings - vertical)
		rotation			 -  text rotation angle (negative is clock wise)
	---------------------------------------------------------------------------------------*/	
	text(x,y,text,color="black",font="10px Arial",align="left",baseline="bottom",rotAngle=0) {
		this.context.fillStyle  = color;
		this.context.font 	  	= font ;
		this.context.textAlign  = align ; // Can be left/rigth/center
		this.context.textBaseline = baseline; // Can be top/bottom/middle/alphabetic/hanging
		this.transformXY(x,y);
		if (rotAngle != 0 ){ 
		   var xPx = this.ucpxTransX(this.xLT);
			var yPx = this.ucpxTransY(this.yLT);
			this.context.translate(xPx,yPx);
			this.context.rotate(-rotAngle*Math.PI/180.);
			this.context.translate(-xPx,-yPx);
		}
		this.context.fillText(text,this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		if (this.trace) console.log ("text " +x +" " +y +" " + text);
		if (rotAngle != 0) {
			this.context.setTransform(1, 0, 0, 1, 0, 0);
		}
	} 

	/*-------------------------------------------------------------------------------------
	Purpose: draw a marker
	Input
		x,y 	- 	marker position
		type  (optional)	-   Marker to draw, can be one of
								cross, dot, circle, star
								(please do not use the other types (to be removed))
								
		color (optional)	-	a web color name or a hue indeks [0,360]
	---------------------------------------------------------------------------------------*/		
	marker(x,y,type="cross",color="black",font="10px Arial") {
		this.context.font = font ;
		if (Number(color)){
			var colstring = 'hsl('+color.toFixed(0) +',100%,50%)';
			this.context.fillStyle = colstring;
		} else { 
			this.context.fillStyle = color;
		}
		this.context.textAlign = "center" ;
		this.context.textBaseline = "middle";
		this.transformXY(x,y);
		
		if (type == "cross") {
			this.context.fillText("X",this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		}
		else if (type == "dot") {
			this.context.fillText(".",this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		}
		else if (type == "circle") {
			this.context.fillText("O",this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		}
		else if (type == "star") {
			this.context.fillText("*",this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		}
		else if (type == "axXmarkerD") {
			var size = (this.ucY2-this.ucY1)/30.
			this.moveTo(x,y); 
			this.lineTo(x,y-size);
			this.textAdvanced(x,y-1.5*size,parseFloat(x.toFixed(3)),"black","12px Arial","center","top");
		}
		else if (type == "axXmarkerU") {
			var size = (this.ucY2-this.ucY1)/30.
			this.moveTo(x,y); 
			this.lineTo(x,y+size);
			this.textAdvanced(x,y+1.5*size,parseFloat(x.toFixed(3)),"black","12px Arial","center","bottom");
		}
		else if (type == "axYmarkerL") {
			var size = (this.ucX2-this.ucX1)/40.
			this.moveTo(x,y); 
			this.lineTo(x-size,y);
			this.textAdvanced(x-1.5*size,y,parseFloat(y.toFixed(3)),"black","12px Arial","right","middle");
			
		}
		else if (type == "axYmarkerR") {
			var size = (this.ucX2-this.ucX1)/40.
			this.moveTo(x,y); 
			this.lineTo(x+size,y);
			this.textAdvanced(x+1.5*size,y,parseFloat(y.toFixed(3)),"black","12px Arial","left","middle");
			
		}
		if (this.trace) console.log ("marker " +x +" " +y);
	} 
	//
	//---Section of functions related to drawing coordinate systems.
    //
	drawBoundary(color="black"){ // Draws boundary of UMC
		this.rectangle(this.ucX1,this.ucY1,this.ucX2,this.ucY2,color);
	} 

	drawXgrid(color="black",increment=1,labels="no",style="dotted",decimal=2,adjust= "no"){ //Uses x-range to draw a vertical lines (option to annotate)
		var x1,x2;
		if (adjust === "yes"){ 
			x1 = Math.floor(this.ucX1);
			x2 = Math.ceil(this.ucX2);
		}
		else {
			x1 = this.ucX1;
			x2 = this.ucX2;	
		}
	// Draw vertical lines
		this.context.beginPath();
		this.context.lineWidth = 1;
		this.context.strokeStyle = color;
		
		if (style == "dotted") this.context.setLineDash([2,3]);
		else this.context.setLineDash([]);
		
		for (var x=x1;x<=x2;x=x+increment){
			this.moveTo(x,this.ucY1);
			this.lineTo(x,this.ucY2);
		}	 
		this.context.stroke();
		this.context.setLineDash([]);
		
	// Draw labels
		if (labels="yes"){ 
			for (var x=x1;x<=x2;x=x+increment){
				this.text(x,this.ucY1,x.toFixed(decimal), "black", "10px Arial","center","top" );
			}	
		}
	} 
	
	drawYgrid(color="black",increment=1,labels="no",style="dotted",decimal=2,adjust="no"){ //Uses y-range to draw a vertical lines (option to annotate)
		var y1,y2;
		if (adjust === "yes"){ 
			y1 = Math.floor(this.ucY1);
			y2 = Math.ceil(this.ucY2);
		}
		else {
			y1 = this.ucY1;
			y2 = this.ucY2;			
		}
	// Draw horisontal lines
		this.context.beginPath(); 
		this.context.lineWidth = 1;
		this.context.strokeStyle = color;
		
		if (style == "dotted") this.context.setLineDash([2,3]);
		else this.context.setLineDash([]);
		
		for (var y=y1;y<=y2+0.001;y=y+increment){
			this.moveTo(this.ucX1,y);
			this.lineTo(this.ucX2,y);
		}
		this.context.stroke();
		this.context.setLineDash([]);
	// Draw labels
		if (labels == "yes"){ 
			for (var y=y1;y<=y2;y=y+increment){
				this.text(this.ucX1,y,y.toFixed(decimal)+" ", "black", "10px Arial","right","middle" );
			}
		}
	} 
	/*-------------------------------------------------------------------------------------
	Purpose: map a value to a color index in a continous color scale.
			 Color maps available 
				"red_blue"
				"blue_red"
			 and can be set by changing the e2d.colormap attribute to one of the above.
			 Also a value range need to be provided. Change the attributes
				e2d.colValue1 and 
				e2d.colValue2

	Input
		x,y 	- 	marker position
		type  (optional)	-   Marker to draw, can be one of
								cross, dot, circle, star
								(please do not use the other types (to be removed))
								
		color (optional)	-	a web color name or a hue indeks [0,360]
	---------------------------------------------------------------------------------------*/	

	mapToColorIndex(value){ // 
		var hueIndeks = 0;
		var opsjon;

		if (this.colormap === "red_blue"){ 
			hueIndeks = 10+((value-this.colValue1)/(this.colValue2 - this.colValue1))*300;
		} else {
			hueIndeks = 310 - ((value-this.colValue1)/(this.colValue2 - this.colValue1))*300;
		}
		if (hueIndeks <  10 ) hueIndeks = 10;
		if (hueIndeks > 310 ) hueIndeks = 310;
	return hueIndeks;
	} 
	//-------------------------------------------------------------------------------------------------
	//---OBJECT INTERNAL utilities for mapping and coordinate transformations
	//-------------------------------------------------------------------------------------------------
	dataRange(xdata,ydata){ // Find ranges, return 4 values in array
		var x1 = +99999999;
		var x2 = -99999999;
		for (var i=0; i < xdata.length;i++){
			if (xdata[i] > x2 ) x2 = xdata[i] ;
			if (xdata[i] < x1 ) x1 = xdata[i] ;
		}
		var y1 = +99999999;
		var y2 = -99999999;
		for (var i=0; i < ydata.length;i++){
			if (ydata[i] > y2 ) y2 = ydata[i] ;
			if (ydata[i] < y1 ) y1 = ydata[i] ;
		}
		return [x1,x2,y1,y2];
	} 

	mc2px (x,y) { // Transform from MCC to PXC
		var xPix,yPix;
		var xt,yt;
		var vpXoffset = this.ncX1*(this.canvas.width-2*this.xMargin);
		var vpYoffset = this.ncY1*(this.canvas.height-2*this.yMargin);
		if (this.useMatrix) {
			xt = x*this.matrixA+y*this.matrixB+this.matrixC;
			yt = x*this.matrixD+y*this.matrixE+this.matrixF;
		}
		else {
			xt = x; yt=y;
		}
		xpix = (xt-this.ucX1)/(this.ucX2-this.ucX1)*this.xScale+this.xMargin+vpXoffset; 
		yPix = this.canvas.height-((yt-this.ucY1)/(this.ucY2-this.ucY1)*this.yScale+this.yMargin+vpYoffset); 
		return [xPix,yPix];
	} 

	px2nc (xpx,ypx) {// Transform from pixel to Normalised coordinates
		var xnc,ync;
		var pixW = this.canvas.width - 2*this.xMargin;
		var pixH = this.canvas.height - 2*this.yMargin;
		xnc = ((xpx-this.xMargin)/pixW) ;
		ync = 1.0-((ypx-this.yMargin)/pixH) ; 
		return [xnc,ync];
	} 

	px2wc (x,y) {// Transform from pixel to window coordinates

		var nc = [], xWin,yWin;
		var ncDiffX = (this.ncX2-this.ncX1);
		var wiDiffX = (this.ucX2-this.ucX1);
		var ncDiffY = (this.ncY2-this.ncY1);
		var wiDiffY = (this.ucY2-this.ucY1);
		nc = this.px2nc(x,y); // Transform to normalised coordinates
		
		xWin = this.ucX1+((nc[0]-this.ncX1)/ncDiffX)*wiDiffX;
		yWin = this.ucY1+((nc[1]-this.ncY1)/ncDiffY)*wiDiffY;
		
		return [xWin,yWin];
	}
	
	px2mc (x,y) {// Transform from pixel to model coordinates
		var wc = [];
		var xt,yt;
		wc = this.px2wc(x,y);
		if (this.useMatrix) {
			var imA,imB,imC,imD,imE,imF;
			imA = 1/this.matrixA;
			imB = this.matrixB/(this.matrixA*(this.matrixB*this.matrixD/this.matrixA) - this.matrixE);
			imC = -((this.matrixB*(((this.matrixC*this.matrixD)/this.matrixA)-this.matrixF))/
				   (this.matrixA*this.matrixE-this.matrixB*this.matrixD) + this.matrixC/this.matrixA);
			xt = wc[0]*imA+wc[1]*imB+imC;
			
			var AEmBD;
			AEmBD = this.matrixA*this.matrixE-this.matrixB*this.matrixD;
			imD = -(this.matrixD/AEmBD );
			imE =   this.matrixA/AEmBD ;
			imF =  (this.matrixC*this.matrixD-this.matrixF)/AEmBD;
			yt = wc[0]*imD+wc[1]*imE+imF;
		}
		else {
			xt = wc[0]; yt=wc[1];
		}
		return [xt,yt];
	}

//-------------------------------------------------------------------------------------------------
//--- Next to be removed (maybe)... Do not use in new development
//-------------------------------------------------------------------------------------------------
	transformXY (x,y) {
		if (this.useMatrix) {
			this.xLT = x*this.matrixA+y*this.matrixB+this.matrixC;
			this.yLT = x*this.matrixD+y*this.matrixE+this.matrixF;
		}
		else {
			this.xLT = x; this.yLT=y;
		}
	} 

	ucpxTransX (x){
		var _vpXoffset = this.ncX1*(this.canvas.width-2*this.xMargin);
		var _x = (x-this.ucX1)/(this.ucX2-this.ucX1)*this.xScale +this.xMargin + _vpXoffset; // UMC->PXC 
		return _x;
	} 

	ucpxTransY (y){
		var _vpYoffset = this.ncY1*(this.canvas.height-2*this.yMargin);
		var _y = this.canvas.height - ((y-this.ucY1)/(this.ucY2-this.ucY1)*this.yScale +this.yMargin + _vpYoffset); // UC->PXC 
		return _y;
	} 
		
	canvasArea(xlow,xhigh,ylow,yhigh){ // Set canvas drawing area. Input pixels.
		this.ncX1 = (xlow -this.xMargin)/(this.canvas.width - 2* this.xMargin);
		this.ncX2 = (xhigh-this.xMargin)/(this.canvas.width - 2* this.xMargin);	
		this.ncY1 = (yhigh-this.canvas.height + this.yMargin)/(2*this.yMargin-this.canvas.height);
		this.ncY2 = (ylow -this.canvas.height + this.yMargin)/(2*this.yMargin-this.canvas.height);
		
		this.xScale = (this.ncX2-this.ncX1)*(this.canvas.width-2*this.xMargin);
		this.yScale = (this.ncY2-this.ncY1)*(this.canvas.height-2*this.yMargin);
		
		if (this.print) console.log ("NDC " ,this.ncX1,this.ncX2,this.ncY1,this.ncY2 );
		if (this.print) console.log ("Scaling " +this.xScale +" " +this.yScale );
		if (this.print) console.log ("Margin " +this.xMargin +" " +this.yMargin);
	} 
 
	textAdvanced(x,y,text,color,font,textAlign,textBaseline) { // Will be removed. Use text()
		this.context.font = font ;
		this.context.fillStyle = color;
		this.context.textAlign = textAlign ;           // Can be left/rigth/center
		this.context.textBaseline = textBaseline;      // Can be top,bottom,middle,left,right
		this.transformXY(x,y);
		this.context.fillText(text,this.ucpxTransX(this.xLT),this.ucpxTransY(this.yLT));
		if (this.trace) console.log ("text " +x +" " +y +" " + text);
	} 
 
	windowAxes1() {
	    var ucX1,ucX2,ucY1,ucY2;
		ucX1 = this.ucX1; ucX2 = this.ucX2;
		ucY1 = this.ucY1; ucY2 = this.ucY2;
		this.context.beginPath();
		this.context.strokeStyle = "black";
		this.moveTo (ucX1,ucY1);
		this.lineTo (ucX2,ucY1);
		this.marker(ucX1,ucY1,"axXmarkerD");
		this.marker(ucX2,ucY1,"axXmarkerD");
		
		this.moveTo (ucX1,ucY1);
		this.lineTo (ucX1,ucY2);
		this.marker(ucX1,ucY1,"axYmarkerL","black");
		this.marker(ucX1,ucY2,"axYmarkerL","black");
		this.context.stroke();
		
	} 

	windowAxes2() {
		var ucX1,ucX2,ucY1,ucY2;
		ucX1 = this.ucX1; ucX2 = this.ucX2;
		ucY1 = this.ucY1; ucY2 = this.ucY2;
		
		this.context.beginPath();
		this.moveTo (ucX1,ucY2);
		this.lineTo (ucX2,ucY2);
		this.marker(ucX1,ucY2,"axXmarkerU"); // Egentlig opp.....
		this.marker(ucX2,ucY2,"axXmarkerU");
		
		this.moveTo (ucX2,ucY1);
		this.lineTo (ucX2,ucY2);
		this.marker(ucX2,ucY1,"axYmarkerR"); // Egentli ned...
		this.marker(ucX2,ucY2,"axYmarkerR");
		this.context.stroke();
		
	} 
	
	drawXaxis(){	//Draw x-axis for given xRange defined
		this.windowAxes1();
	} 

	drawYaxis(){ //Draw y-axis for given yRange
		this.windowAxes2();
	}
	
}// END EASY2D GRAPHICS LIBRARY
 
	

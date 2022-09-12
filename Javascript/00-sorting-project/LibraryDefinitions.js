
/* CanvasPositionTranslator is a class containing methods for translating the
pixel-coordinates in a canvas to normalized world-coordinates. Also includes
methods for drawing lines and geometric shapes. Methods included are:  */
const cpt = new CanvasPositionTranslator(canvasID, canvasWidth, canvasHeight);

//Defines the range of values for the x-axis
cpt.xRange(x1, x2);

//Defines the range of values for the y-axis
cpt.yRange(y1, y2);

//Defines the spacing between the canvas-edge and coordinate-plot for the x-axis
cpt.xMargin(left, right);

//Defines the spacing between the canvas-edge and coordinate-plot for the y-axis
cpt.yMargin(bottom, right);

//Defines how much the coordinate-plot should be rotated relative to the canvas
cpt.rotate(angle);

//Draws lines showing the xy-positions
cpt.drawGridlines(showOrigin, showPerimeter);

//Three methods that work together to create unique shapes.
//drawLine can be run several times between drawLineStart and drawLineStop
cpt.drawLineStart(x, y);
cpt.drawLine(x, y, colour, width, dotted);
cpt.drawLineEnd(fill);

//Draws a line-segment from point1 to point2
cpt.drawLineSegment(x1, y1, x2, y2, colour, width, dotted);

//Writes text
cpt.text(x, y, text, colour, font, angle);

//Draws shapes
cpt.drawSquare(x1, y1, x2, y2, colour, fill);
cpt.drawCircle(x, y, xRadius, yRadius, colour, fill);
cpt.drawPolygon(xArray, yArray, colour, fill);





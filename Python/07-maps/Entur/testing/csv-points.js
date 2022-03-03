
// const createEnturClient = require("./node_modules/@entur/sdk").default

// const Plotly = require("./node_modules/").default
// import * as Plotly from 'plotly.js';
const Plotly = require("plotly")("tepohi", "4y47opcRepoDkdGXU3R9")

// data = [
// 	{
// 		type: 'scatter',  // all "scatter" attributes: https://plotly.com/javascript/reference/#scatter
// 		x: [1, 2, 3],     // more about "x": #scatter-x
// 		y: [3, 1, 6],     // #scatter-y
// 		marker: {         // marker is an object, valid marker keys: #scatter-marker
// 			color: 'rgb(16, 32, 77)' // more about "marker.color": #scatter-marker-color
// 		}
// 	},
// 	{
// 		type: 'bar',      // all "bar" chart attributes: #bar
// 		x: [1, 2, 3],     // more about "x": #bar-x
// 		y: [3, 1, 6],     // #bar-y
// 		name: 'bar chart example' // #bar-name
// 	}
// ];

layout = {                     // all "layout" attributes: #layout
	title: 'simple example',  // more about "layout.title": #layout-title
	xaxis: {                  // all "layout.xaxis" attributes: #layout-xaxis
		title: 'time'         // more about "layout.xaxis.title": #layout-xaxis-title
	},
	annotations: [            // all "annotation" attributes: #layout-annotations
		{
			text: 'simple annotation',    // #layout-annotations-text
			x: 0,                         // #layout-annotations-x
			xref: 'paper',                // #layout-annotations-xref
			y: 0,                         // #layout-annotations-y
			yref: 'paper'                 // #layout-annotations-yref
		}
	]
}

data = [
	{
		type: "scattermapbox",
		lat:[],
		lon:[],
		mode:"markers",
		marker: {
			size: 14
		}
	}
]

layout = {
	title: "",
	xaxis: {
		title: "time"
	},
	hovermode: "closest",
	mapbox : {
		bearing: 0,
		pitch: 0,
		zoom: 5,
		center: {
			lon: 10.75,
			lat: 59.93
		},
		style: "carto-positron"
	},
}

Plotly.plot(
	data,
	layout,
	function (err, msg) {
		if (err) return console.log(err);
		console.log(msg);
	}
)

// Plotly.newPlot("", data, layout)
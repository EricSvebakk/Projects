
// import createEnturClient from "@entur/sdk"
const createEnturClient = require("@entur/sdk").default

const createCsvWriter = require("csv-writer").createObjectCsvWriter

// =========================================================================================
const csvWriter = createCsvWriter(
	{
		path: "routes.csv",
		header: [
			{ id: "lon", title: "Lon" },
			{ id: "lat", title: "Lat" },
			{ id: "name", title: "Name" },
			{ id: "mode", title: "Mode" },
			{ id: "id", title: "Id" },
		]
	}
);

const enturClient = createEnturClient({
	clientName: "aCuriousStudent-aCoolApp",
});

console.log("Hello World!")

// =========================================================================================
function decode(encoded) {

	// array that holds the points

	var points = []
	var index = 0, len = encoded.length;
	var lat = 0, lng = 0;
	
	while (index < len) {
		var b, shift = 0, result = 0;
		
		do {
			b = encoded.charAt(index++).charCodeAt(0) - 63;//finds ascii                                                                                    //and substract it by 63
			result |= (b & 0x1f) << shift;
			shift += 5;
			
		} while (b >= 0x20);

		var dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
		lat += dlat;
		shift = 0;
		result = 0;
		
		do {
			b = encoded.charAt(index++).charCodeAt(0) - 63;
			result |= (b & 0x1f) << shift;
			shift += 5;
			
		} while (b >= 0x20);
		
		var dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
		lng += dlng;

		points.push({ latitude: (lat / 1E5), longitude: (lng / 1E5) })

	}
	
	return points
}

// =========================================================================================
async function findTrip() {
	try {
		const trip = await enturClient.findTrips("Oslo S", "Blindern vgs.",)

		console.log(trip)
		
		const data = []
		let m = 0
		let n = 0
		
		for (let i = 0; i < trip.length; i++) {
			
			n++
			console.log("========================================")
			
			for (let j = 0; j < trip[i].legs.length; j++) {
				
				m++
				
				if (false) {
					console.log(trip[0].legs[j])
					
				} else {
					
					// let lon = trip[i].legs[j].fromPlace.longitude
					// let lat = trip[i].legs[j].fromPlace.latitude
					// let name = trip[i].legs[j].fromPlace.name
					// let sjid = n
					
					// console.log(lon + ", " + lat + ", " + name + ", " + mode + ", " + sjid)

					// INTERMEDIATE ESTIMATED CALLS
					if (true) {
						console.log(trip[i].legs[j].intermediateEstimatedCalls)
						
						// console.log(trip[i].legs[j].situations)

					} else {
						if (trip[i].legs[j].intermediateEstimatedCalls.length > 0) {
							for (let l = 0; l < trip[i].legs[j].intermediateEstimatedCalls.length; l++) {

								// console.log(trip[i].legs[j].intermediateEstimatedCalls[l].quay)

								let IEC = trip[i].legs[j].intermediateEstimatedCalls[l]

								lon = IEC.quay.stopPlace.longitude
								lat = IEC.quay.stopPlace.latitude
								name = IEC.quay.name
								mode = IEC.serviceJourney.transportSubmode
								// sjid = IEC.serviceJourney.id
								sjid = n

								console.log(lon + ", " + lat + ", " + name + ", " + mode + ", " + sjid)
							}
						}
					}
					
					// SITUATIONS
					// for (let l = 0; l < trip[i].legs[j].situations.length; l++) {
					// 	console.log(trip[i].legs[j].situations[l]);
					// }
					
					
					// POINTS ON LINK
					if (trip[i].legs[j].pointsOnLink != undefined) {
						
						var lname, lmode, lid;
						
						let line = trip[i].legs[j].line
						
						if (line != undefined) {
							lname = line.name
							lmode = line.transportMode
							lid = line.id
						}
						
						else {
							lname = trip[i].legs[j].fromPlace.name + " - " + trip[i].legs[j].toPlace.name
							lmode = "foot"
							lid = 0
						}

						let points = trip[i].legs[j].pointsOnLink.points;
						
						text = decode(points);
						
						for (let l = 0; l < text.length; l++) {
							
							data.push({
								lon: text[l].longitude,
								lat: text[l].latitude,
								name: lname,
								mode: lmode,
								id: n + "-" + m + "-" + lid
							})
							// console.log(text[l].longitude + ", " + text[l].latitude + ",,," + sjid);
						}
						
					}
					
					// TEXT
					// lon = trip[i].legs[j].toPlace.longitude
					// lat = trip[i].legs[j].toPlace.latitude
					// name = trip[i].legs[j].toPlace.name
					// mode = trip[i].legs[j].mode
					// sjid = n

					// SERVICE JOURNEY
					// if (trip[i].legs[j].serviceJourney != undefined) {
					// 	sjid = trip[i].legs[j].serviceJourney.id
					// }

					// console.log(lon + ", " + lat + ", " + name + ", " + mode + ", " + sjid)
				}

				console.log("----------------------------------------")
			}

			// console.table(data)
		}
		
		csvWriter.writeRecords(data).then(()=>console.log("CSV-file created successfully"))

	}
	catch (error) {
		console.log(error)
	}
}

// =========================================================================================
findTrip()
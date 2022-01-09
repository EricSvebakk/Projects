
const createEnturClient = require("./node_modules/@entur/sdk").default
// import createEnturClient from "@entur/sdk"

console.log("Hello World!")

const enturClient = createEnturClient({
	clientName: "aCuriousStudent-aCoolApp",
})

// console.log(enturClient)

async function findTrip() {
	try {
		const trip = await enturClient.findTrips("Oslo S", "Blindern vgs.",)
		
		console.log(trip)
				
		let n = 0
		
		for (let i = 0; i < trip.length; i++) {
			
			const data = []
			
			n++
			
			console.log("========================================")
			for (let j = 0; j < trip[i].legs.length; j++) {
				
				
				if (false) {
					console.log(trip[0].legs[j])
					// let journey = trip[0].legs[i].serviceJourney.journeyPattern
					// console.log(journey)
					
				} else {
					
					
					let lon = trip[i].legs[j].fromPlace.longitude
					let lat = trip[i].legs[j].fromPlace.latitude
					let name = trip[i].legs[j].fromPlace.name
					let mode = trip[i].legs[j].mode
					let sjid = n
					
					// if (trip[i].legs[j].serviceJourney != undefined) {
					// 	sjid = trip[i].legs[j].serviceJourney.id
					// }
					
					console.log(lon + ", " + lat + ", " + name + ", " + mode + ", " + sjid)
					
					if (false) {
						console.log(trip[i].legs[j].intermediateEstimatedCalls)
						
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
					
					lon = trip[i].legs[j].toPlace.longitude
					lat = trip[i].legs[j].toPlace.latitude
					name = trip[i].legs[j].toPlace.name
					mode = trip[i].legs[j].mode
					sjid = n
					
					// if (trip[i].legs[j].serviceJourney != undefined) {
					// 	sjid = trip[i].legs[j].serviceJourney.id
					// }
					
					console.log(lon + ", " + lat + ", " + name + ", " + mode + ", " + sjid)
				}
				
				console.log("----------------------------------------")
			}
			
			// console.table(data)
		}
		
	}
	catch (error) {
		console.log(error)
	}
}

async function getVenue() {
	try {
		// const features = await enturClient.
		// const venue = await enturClient.getFeatures("Blindern vgs.")
		const venue = await enturClient.getFeatures("Oslo S")
		console.log(typeof(venue) + " " + venue.length)
		// console.log(venue)
		
		for (let i = 0; i < venue.length; i++) {
			console.log(venue[i].properties.name)
			console.log(venue[i].properties.street)
			console.log(venue[i].properties.county)
			console.log(venue[i].properties.layer)
			console.log(venue[i].properties.category)
			console.log("\n\n")
		}
		
	}
	catch (error) {
		console.log(error)
	}
}

findTrip()
// getVenue()
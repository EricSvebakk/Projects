
# import pandas as pd
# import sys
import json

FILENAME = "../municipalityData"



with open('../norway2013mun.json') as file1:
	
	try:
		open(f"{FILENAME}.json", 'w').close()
	except FileNotFoundError:
		pass
	
	with open(f"{FILENAME}.json", "a") as file2:
		
		df = json.load(file1)
	
		data = {
			"type": "FeatureCollection",
			"features": []
		}
		
		id = 0
		
		for i in range(len(df["features"])):
			
			temp = df['features'][i]['properties']
			geometry = df['features'][i]['geometry']
			
			data['features'].append({
				"type": "Feature",
				"properties": {
					"navn": temp['NAVN'],
					"fylke": temp['fylke'],
					"kommune": temp['kommnr'],
					"areal": temp['Shape_Area']
				},
				"geometry": {
					"type": geometry['type'],
					# "id": temp['kommnr'],
					"coordinates": geometry['coordinates']
				}
			})
			
			id += 1
		
		json.dump(data, file2, indent=4)

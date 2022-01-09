
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, shape
from geopandas.tools import sjoin
import json
import time as t


df = pd.read_csv("../data/Location History.csv")
# df = pd.read_csv("../data/initialtesting/temp2.csv")


with open("../municipalityData.json") as file:
	gdf = json.load(file)

#=============================================================

start = t.time()

rows = []

for i in range(len(df)):
	lon = df["longitude"].iloc[i]
	lat = df["latitude"].iloc[i]
	year = df["year"].iloc[i]
	time = df["time"].iloc[i]
	
	rows.append([
		Point(lon, lat),
		year,
		time,
	])

df = pd.DataFrame(
	[*rows],
	columns=[
		"points",
		"year",
		"time",
	]
)

rows = []

for i in range(len(gdf["features"])):
	
	temp = gdf["features"][i]
	poly = shape(temp["geometry"])
	
	for year in df["year"].unique():
		numPoints = 0
		
		points = df[df["year"] == year]
		
		numPoints = gpd.sjoin(points, poly, op="within")
		
		# for j in range(len(points)):
		
		# 	if poly.contains(points["points"].iloc[j]):	
		# 		numPoints += 1
		# 		# print("yay")

		rows.append([
			temp["properties"]["navn"],
			temp["properties"]["kommune"],
			temp["properties"]["fylke"],
			year,
			numPoints,
		])


df = pd.DataFrame(
	[*rows],
	columns=[
		"kommuneNAVN",
		"kommuneID",
		"fylkeID",
		"aar",
		"hyppighet",
	]
)

end = t.time()

print(f"\nElapsed time: {(end-start):.2f}s\n")

df.to_csv("MYTESTDATA3.csv", index=False)



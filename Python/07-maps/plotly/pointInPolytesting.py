
import geopandas as gpd
import pandas as pd
import time as t

# df = pd.read_csv("../data/initialtesting/temp2.csv")
df = pd.read_csv("../data/Location History.csv")

gdf = gpd.read_file("../data/municipalityData.json")

#=============================================================

start = t.time()

allPoints = gpd.GeoDataFrame(
	df,
	geometry=gpd.points_from_xy(df["longitude"],df["latitude"]),
	crs=4326
)

rows = []
for i in range(len(gdf)):

	poly = gdf[gdf["navn"] == gdf["navn"].iloc[i]]
	
	for year in df["year"].unique():
		
		points = allPoints[allPoints["year"] == year]
		
		numPoints = gpd.sjoin(points, poly, predicate="within")
		
		rows.append([
			poly.at[i, "navn"],
			poly.at[i, "kommune"],
			poly.at[i, "fylke"],
			year,
			len(numPoints),
		])

#=============================================================

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

#=============================================================

end = t.time()

print(f"\nElapsed time: {(end-start):.2f}s\n")

df.to_csv("MYTESTDATA2.csv", index=False)



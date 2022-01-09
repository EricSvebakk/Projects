
from json import encoder
import pandas as pd
import json
import shapely.geometry
import geojson
import geopandas as gpd

# MIN AND MAX ALTITUDE
# print(df.loc[df['altitude'].idxmin()])
# print(df.loc[df['altitude'].idxmax()])

# ========================================================================================
# df = pd.read_json(f"{FILENAME}.json")
# print(df["features"][0]["properties"]["navn"])

# ========================================================================================
# df = pd.read_csv("../munip.csv", dtype={"region":str})
# df[["region","name"]] = df["region"].str.split(" ", n = 1, expand=True)
# df.to_csv("../munip.csv", index=False)

# ========================================================================================
# FILENAME = "../norway2013mun"

# with open(f"{FILENAME}.json") as file:
# 	df = json.load(file)

# df2 = pd.read_csv("../fylker-kommuner-2019-2020-alle.csv",
#                   dtype={"Kommunenr. 2019": str, "Kommunenr. 2020":str}
# )

# # print(df)
# for i in range(len(df["features"])):
# 	for j in range(len(df2)):
		
# 		if df["features"][i]["geometry"]["id"] == df2["Kommunenr. 2019"].iloc[j]:
# 			# print(i, j, df2["Kommunenr. 2019"].iloc[j])
			
# 			df["features"][i]["geometry"]["id"] = df2["Kommunenr. 2020"].iloc[j]
# 			df["features"][i]["properties"]["kommune"] = df2["Kommunenr. 2020"].iloc[j]
# 			df["features"][i]["properties"]["fylke"] = df2["Kommunenr. 2020"].iloc[j][:2]

# try:
# 	open(f"{FILENAME}2.json", 'w').close()
# except FileNotFoundError:
# 	pass

# with open(f"{FILENAME}2.json", "a") as file2:
# 	json.dump(df, file2)

# ========================================================================================
# df = pd.read_csv(f"../munip.csv")

# for i in range(len(df)):
	
# 	if (df["type of area"].iloc[i] == 2):
# 		df.drop(labels=[i])
		
# df["type of area"] = df["type of area"].str.split(" ", n = 1, expand=True)[0]
# df = df[df["type of area"] == 1]
	
# df.to_csv("../munip.csv", index=False)

# ========================================================================================
# df = pd.read_csv(f"../fylker-kommuner-2019-2020-alle.csv")
# df2 = pd.read_csv(f"../munip.csv")

# df = df.assign(name=pd.Series(range(len(df))).values)


# for i in range(len(df)):
# 	for j in range(len(df2)):
		
# 		if df["region"].iloc[i] == df2["Kommunenr. 2020"].iloc[j]:
# 			df["navn"].iloc = df2["Kommunenavn 2020"].iloc[j]


# df.to_csv("../munip.csv", index=False)

# ========================================================================================

# df1 = pd.read_json(f"../municipalityData.json")
# df2 = pd.read_csv(f"../munip.csv")
# df3 = pd.read_csv(f"../fylker-kommuner-2019-2020-alle.csv")


# # get alle kommune names
# data = []
# for i in range(len(df1["features"])):
# 	data.append(df1["features"][i]["properties"]["navn"].lower())


# print(len(data))

# # reduce data to outdated kommune names only
# for i in range(len(df2)):
# 	if (df2["name"].iloc[i].__str__().lower() in data):
# 		data.remove(df2["name"].iloc[i].__str__().lower())

# print(len(data))
# print(len(df1["features"]), len(df2["region"]))

# data2 = {}

# n = 0
# # create dictionary of all new kommunes and their corresponding sub-kommune
# for i in range(len(df3)):
	
# 	if (not data2.__contains__(df3["Kommunenavn 2020"].iloc[i].lower())):
# 		data2[df3["Kommunenavn 2020"].iloc[i].lower()] = []
	
# 	if df3["Kommunenavn 2019"].iloc[i].__str__().lower() in data:
# 		n += 1
# 		data2[df3["Kommunenavn 2020"].iloc[i].lower()].append(df3["Kommunenavn 2019"].iloc[i].lower())

# print(n)

# newGEOJSON = {
# 	"type": "FeatureCollection",
# 	"features": [],
# }
	
# for i in data2.keys():

# 	# Shows new kommune
# 	if (len(data2[i]) != 0):
# 		print(i, data2[i])

# 	# polygons = []
	
# 	# for l in range(len(df1)):
# 	# 	if (df1["features"][l]["properties"]["navn"].lower() in data2[i]):
			
# 	# 		print(l, df1["features"][l]["geometry"])
# 	# 		temp = shapely.geometry.shape(df1["features"][l]["geometry"])
			
# 	# 		if (temp.geom_type == "Polygon"):
# 	# 			polygons.append(temp)
				
			
# 	# 		# shapely.geometry.asPolygon
	

# 	# if (len(polygons) != 0):
# 	# 	print(polygons)
			
# 	# 	newPolygon = polygons[0]
# 	# 	for j in range(1, len(polygons)):
# 	# 		newPolygon = newPolygon.union(polygons[j])
		
# 	# 	geojson_out = geojson.Feature(geometry=newPolygon, properties={})

# 	# 	for j in range(len(df3)):
# 	# 		if df3["Kommunenavn 2020"].iloc[j] == i:
				
# 	# 			newGEOJSON['features'].append({
# 	# 				"type": "Feature",
# 	# 				"properties": {
# 	# 					"navn": i,
# 	# 					"fylke": df3["Fylkesnr. 2020"],
# 	# 					"kommune": df3["Kommunenr. 2020"],
# 	# 				},
# 	# 				"geometry": geojson_out.geometry
# 	# 			})

# with open('Merged_Polygon.json', 'w') as outfile:
#     json.dump(newGEOJSON, outfile,ensure_ascii=False, indent=3)

# ========================================================================================

# df1 = pd.read_json(f"../municipalityData.json")
# df2 = pd.read_csv(f"../munip.csv")
# df3 = pd.read_csv(f"../fylker-kommuner-2019-2020-alle.csv")

# df2 = df2.drop("type of area", 1)
# df2 = df2.drop("contents", 1)
# df2 = df2.drop("year", 1)

# for j in range(len(df2)):
# 	for i in range(len(df3)):
	
# 		if (df2["region"].iloc[j] == df3["Kommunenr. 2020"].iloc[i]):
			
# 			df2.loc[j, "region"] = f"{df3['Kommunenr. 2019'].iloc[i]:04}"


# # # get alle kommune names
# data = []
# for i in range(len(df1["features"])):
# 	data.append(df1["features"][i]["properties"]["navn"].lower())

# print(len(data))

# # # reduce data to outdated kommune names only
# for i in range(len(df2)):
# 	if (df2["name"].iloc[i].__str__().lower() in data):
# 		data.remove(df2["name"].iloc[i].__str__().lower())

# print(data)

# for i in range(len(df1)):
# 	# for j in range(len(df2)):
	
# 	if (df1["features"][i]["properties"]["navn"].lower() in data) and not (df1["features"][i]["properties"]["kommune"] in df2["region"]):
		
# 		# print(df1["features"][i]["properties"]["navn"])
		
# 		df2 = df2.append({
# 			"region": df1["features"][i]["properties"]["kommune"],
# 			"area": 0,
# 			"name": df1["features"][i]["properties"]["navn"]
# 		},ignore_index=True)

			
# print(df2)
# df2.to_csv("../munip3.csv", index=False)

# ========================================================================================

# FILENAME = "../municipalityData"

# df1 = pd.read_json(f"{FILENAME}.json")

# df2 = {
# 	"01": "Østfold ",
#     "02": "Akershus",
# 	"03": "Oslo",
#     "04": "Hedmark",
#     "05": "Oppland",
#     "06": "Buskerud",
#     "07": "Vestfold",
#     "08": "Telemark",
#     "09": "Aust-Agder",
#     "10": "Vest-Agder",
# 	"11": "Rogaland",
#     "12": "Hordaland ",
#     "13": "Bergen",
#     "14": "Sogn og Fjordane",
#     "15": "Møre og Romsdal",
#     "16": "Sør-Trøndelag",
#     "17": "Nord-Trøndelag",
# 	"18": "Nordland",
#     "19": "Troms",
#     "20": "Finnmark"
# }

# rows = []

# for i in range(len(df1)):
	
# 	temp = df1["features"][i]
	
# 	rows.append([
# 		temp["properties"]["kommune"],
# 		temp["properties"]["navn"],
# 		temp["properties"]["fylke"],
# 		df2[temp["properties"]["fylke"]],
# 	])

# df3 = pd.DataFrame(
# 	[*rows],
# 	columns=[
# 		"kommuneID",
# 		"kommuneNAVN",
# 		"fylkeID",
# 		"fylkeNAVN"
# 	]
# )



# try:
# 	open(f"{FILENAME}4.csv", 'w').close()
# except FileNotFoundError:
# 	pass

# df3.to_csv(f"{FILENAME}4.csv", index=False)

# ========================================================================================

level = 1
country = "NZL"
FILENAME = f"gadm36_{country}_{level}"

gdf = gpd.read_file(f"../gadm36_{country}_shp/gadm36_{country}_{level}.shp", encoding="utf-8")

rows = []

for i in range(len(gdf)):

	rows.append([
		f"{i:02}",
		gdf["NAME_1"].iloc[i]
	])

df3 = pd.DataFrame(
	[*rows],
	columns=[
		"fylkeID",
		"fylkeNAVN"
	]
)

df3.to_csv(f"../{FILENAME}.csv", index=False)

# ========================================================================================

# df1 = pd.read_json(f"gpd_norway_geo1.json")

# print(df1)

# df2 = pd.read_csv(f"../munip.csv")
# df3 = pd.read_csv(f"../fylker-kommuner-2019-2020-alle.csv")

# df2 = {
# 	"Ostfold ": "01",
#     "Akershus": "02",
# 	"Oslo": "03",
#     "Hedmark": "04",
#     "Oppland": "05",
#     "Buskerud": "06",
#     "Vestfold": "07",
#     "Telemark": "08",
#     "Aust-Agder": "09",
#     "Vest-Agder": "10",
# 	"Rogaland": "11",
#     "Hordaland ": "12",
#     "Bergen": "13",
#     "Sogn og Fjordane": "14",
#     "Møre og Romsdal": "15",
#     "Sør-Trøndelag": "16",
#     "Nord-Trøndelag": "17",
# 	"Nordland": "18",
#     "Troms": "19",
#     "Finnmark": "20"
# }

# rows = []

# "".capitalize()

# for i in range(len(df1)):

# 	temp = df1["features"][i]

# 	rows.append([
# 		# df2[temp["properties"]["NAME_1"].capitalize()],
# 		temp["properties"]["NAME_1"],
# 	])


# df3 = pd.DataFrame(
# 	[*rows],
# 	columns=[
# 		# "kommuneID",
# 		# "kommuneNAVN",
# 		# "fylkeID",
# 		"fylkeNAVN"
# 	]
# )

# print(df3)
# df3.to_csv("../gpd_temp1.csv", index=True)

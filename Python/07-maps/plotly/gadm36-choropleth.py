
from dash.dependencies import Output
import geopandas as gpd
import pandas as pd

from zipfile import ZipFile
import os

import plotly.express as px
import json
# import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# ========================================================================================

NAME = f"gadm36_NOR"
LEVEL = 2

FILENAME_ZIP = f"{NAME}_shp.zip"
FILENAME_SHP = f"{NAME}_{LEVEL}.shp"


zff = ZipFile(f"../data/{FILENAME_ZIP}")
zff.extractall(f"../data/{NAME}")

gdf = gpd.read_file(f"../data/{NAME}/{FILENAME_SHP}")

for file in zff.namelist():
	os.remove(f"../data/{NAME}/{file}")
os.removedirs(f"../data/{NAME}")

rows = []

# print(gdf)

for i in range(len(gdf)):
	
	rows.append([
		i,
		gdf[f"NAME_{LEVEL}"].iloc[i],
		gdf[f"NAME_{LEVEL-1}"].iloc[i],
	])

df = pd.DataFrame(
	[*rows],
	columns=[
		"ID",
		"NAME",
		"AREA",
	]
)

# gdf.to_json()

# gdf.to_file(f"../{NAME}_{LEVEL}.json")
# df2.to_csv(f"../{NAME}_{LEVEL}.csv", index=False)

# ========================================================================================

# gdf = gpd.read_file("../municipalityData.json").to_json
df = pd.read_csv("MYTESTDATA2.csv", dtype={"fylkeID":int, "kommuneID":str})

with open("../data/municipalityData.json",encoding="utf-8") as file:
	gdf = json.load(file)
	
print(len(df))
print(len(gdf["features"]))

# ========================================================================================

app = dash.Dash(__name__)

app.layout = html.Div([
	dcc.Graph(id="coordinates"),
	# dcc.Slider(
	# 	id="choropleth-slider",
	# 	min=df["hyppighet"].min(),
	# 	max=df["hyppighet"].min(),
	# 	value=df["hyppighet"].min(),
	# 	step=100,
	# 	# width=100
	# 	# vertical=True,
	# 	# verticalHeight=50,
	# ),
	dcc.Input(
		id="choropleth-input",
		type="number",
		min=df["hyppighet"].min(),
		max=5000,
		value=1000,
		# step=100,
	)
])

@app.callback(
	Output("coordinates", "figure"),
	Input("choropleth-input", "value"),
	# Input("choropleth-input", "value"),
)

def update_figure(selected_max):
	# df_filter = df[df["hyppighet"] > selected_max]
	
	fig = px.choropleth_mapbox(df, geojson=gdf,
		animation_frame="aar",
		locations="kommuneID",
		color="hyppighet",
		featureidkey=f"properties.kommune",
		color_continuous_scale="Turbo",
		range_color=(0,selected_max),
		# hovertemplate="""WALLAH""",
		# title="Norway",
		# labels={"NAME_1"},
		hover_data=[
			# "fylkeNAVN",
			"kommuneNAVN",
			# "kommuneID",	
		],
		zoom=4.4,
		center={
			"lon": 17.5,
			"lat": 65.6,
		},
		opacity=1.0,
	)
	
	fig.update_layout(mapbox_style="carto-darkmatter")
	fig.update_layout(width=1000,height=1000)
	fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
	fig.update_traces(marker_line_width=2, marker_line_color="black")
	
	# Hinders Dash from resetting center and zoom
	fig["layout"]["uirevision"] = 10
	
	return fig
	

if __name__ == '__main__':
    app.run_server(debug=True)

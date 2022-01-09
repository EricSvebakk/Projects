
import math
from os import name
from pandas.core.frame import DataFrame
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
import dash

CODE = "RUT"

df1 = pd.read_csv(f"{CODE}/shapes.csv")
df2 = pd.read_csv(f"{CODE}/stops.csv")
df3 = pd.read_csv(f"{CODE}/trips.csv")
df4 = pd.read_csv(f"{CODE}/routes.csv")

# ==========================================================

# PREFIX = "stop"
PREFIX = "shape_pt"

Oslo = {
	f"{PREFIX}_lon": [10.65, 10.85],
	f"{PREFIX}_lat": [59.88, 60.0],
	# "altitude": [0, 800],
}

# for i in Oslo.keys():
# 	df1 = df1.query(f"{i} >= {Oslo[i][0]}")
# 	df1 = df1.query(f"{i} < {Oslo[i][1]}")

# ==========================================================

# # FINDS TRIPS THAT CONTAIN STRING IN TRIP_HEADSIGNS
# filter = df3.loc[df3["trip_headsign"].str.contains("Forskningsparken")]
# filter = filter.loc[df3["shape_id"].notnull()]

# filter = filter.loc[filter["shape_id"].notnull()]
# filter = filter["shape_id"]
# filter = filter.tolist()

# # USE FILTER TO GET VALID POINTS FROM DF1 (shapes.csv)
# df1 = df1.query("shape_id == @filter")

# ------------------------------

TBANE = [1,2,3,4,5]
TRIKK = [11,12,13,17,18,19]
REST = df4

filter = DataFrame(df1)
temp = DataFrame()

filter = df1.loc[df1["shape_id"].str.contains(f"RUT:JourneyPattern:{1}-")]

# print(filter)

for i in TRIKK:
	temp = df1.loc[df1["shape_id"].str.contains(f"RUT:JourneyPattern:{i}-")]
	print(f"RUT:JourneyPattern:{i}-")
	# print(temp)
	filter = filter.append(temp, ignore_index=True)
	
# print(filter)

# df1 = filter

# -------------------------------------

filter_df4 = df4.loc[df4["route_type"] == 704]
filter_df4 = filter_df4["route_id"].tolist()

filter_df3 = df3.loc[df3["route_id"].isin(filter_df4)]
filter_df3 = filter_df3["shape_id"].tolist()

df1 = df1.loc[df1["shape_id"].isin(filter_df3)]


# =============================================================================

# default_linewidth = 2
# highlighted_linewidth_delta = 2

# def update_trace(trace, points, selector):
#     # this list stores the points which were clicked on
#     # in all but one trace they are empty
#     if len(points.point_inds) == 0:
#         return
        
#     for i,_ in enumerate(fig1.data):
#         fig1.data[i]['line']['width'] = default_linewidth + highlighted_linewidth_delta * (i == points.trace_index)

# ===============================================================================

fig1 = go.FigureWidget()

# POINTS
fig2 = px.scatter_mapbox(
	df2,
	lat="stop_lat",
	lon="stop_lon",
	color="vehicle_type",
	color_continuous_scale="rainbow",
	custom_data=["stop_name"],
)

fig2.update_traces(
	hovertemplate=
	"<b>name<b>: %{customdata[0]}<br>" +
	"<b>lat<b>: %{lat}<br>" +
	"<b>lon<b>: %{lon}"
)

# LINES
fig3 = px.line_mapbox(
	df1,
	lat="shape_pt_lat",
	lon="shape_pt_lon",
	color="shape_id",
	custom_data=["shape_id"],
)

fig3.update_traces(
	hovertemplate=
	"<b>name<b>: %{customdata[0]}<br>"+
	"<b>lat<b>: %{lat}<br>"+
	"<b>lon<b>: %{lon}"
)

# # Adds fig2 and fig3 traces to fig1
# for i in fig2.data:
# 	# i.on_click(update_trace)
# 	fig1.add_trace(i)

for i in fig3.data:
	fig1.add_trace(i)
	
fig1.update_layout(mapbox_style="carto-darkmatter")
fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig1.update_layout(width=2000, height=1000)

# ==========================================================

app = dash.Dash(__name__)

app.layout = html.Div([
	dcc.Graph(
		id="coordinates",
		figure=fig1,
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)

# =====================================

# from math import sin, acos, cos

# math.acos()
# math.sin()

# RADIUS_KM = 2

# result = acos(
# 	sin(a.Latitude * 0.0175) *
# 	sin(YOUR_LATITUDE_X * 0.0175) +
# 	cos(a.Latitude * 0.0175)*
# 	cos(YOUR_LATITUDE_X * 0.0175) *
#     cos((YOUR_LONGITUDE_Y * 0.0175) -
# 	(a.Longitude * 0.0175))

# ) *6371 <= RADIUS_KM

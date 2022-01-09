
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from dash import dcc, html
import dash


FILENAME_CSV = "../data/Location History.csv"

df = pd.read_csv(FILENAME_CSV, dtype={"month":int})

# ==========================================================

Oslo = {
	"longitude": [10.5, 11.0],
	"latitude": [58.0, 60.0],
	"altitude": [0, 800],
}

Ålesund = {
	"longitude": [5.5, 8.5],
	"latitude": [62.0, 64],
	"altitude": [0, 800],
}

# AREA = Ålesund

# for i in AREA.keys():
# 	df = df.query(f"{i} >= {AREA[i][0]}")
# 	df = df.query(f"{i} < {AREA[i][1]}")

ZOOM = 5

# fig = go.Figure()

# fig.add_trace(go.Scattermapbox(
# 	# df,
# 	lat=df["latitude"], lon=df["longitude"],
# 	marker=go.scattermapbox.Marker(
		
# 		color="month",
# 	),
# 	# animation_frame="time",
# 	range_color=(1,12),
# 	zoom=ZOOM,
# 	color_continuous_scale="Rainbow",
# 	# hovertemplate=""
# 	# mode=""
# )
# )

# SCATTER LOCATION MAP - PRETTY
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
	color="month",
	# range_color=(1,12),
	# animation_frame="year",
	color_continuous_scale="Agsunset",
	zoom=ZOOM,
	# hovertemplate=""
)

# DENSITY LOCATION MAP - UGLY
# fig = px.density_mapbox(df, lat="latitude", lon="longitude", z="altitude", radius=5, zoom=ZOOM)

fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(width=1000, height=1000)
fig.update_traces(hoverinfo="skip", hovertemplate=None)
# fig.show()

# ==========================================================

app = dash.Dash(__name__)

app.layout = html.Div([
	dcc.Graph(
		id="coordinates",
		figure=fig,
	)
])

if __name__ == '__main__':
    app.run_server(debug=True)

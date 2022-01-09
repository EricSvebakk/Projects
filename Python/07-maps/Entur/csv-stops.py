
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
import dash

df1 = pd.read_csv(f"mystops.csv")

# ==========================================================

# df1 = df1.query("shape_id == @temp")

fig1 = go.FigureWidget()

fig2 = px.line_mapbox(
	df1,
	lat="lat",
	lon="lon",
	color="sjid",
	custom_data=["name"],
)

fig2.update_traces(
	hovertemplate=
	"<b>name<b>: %{customdata[0]}<br>" +
	"<b>lat<b>: %{lat}<br>" +
	"<b>lon<b>: %{lon}"
)

for i in fig2.data:
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



from bokeh.models.callbacks import CustomJS
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import get_provider, CARTODBPOSITRON, STAMEN_TERRAIN_RETINA, CARTODBPOSITRON_RETINA
from pyproj import Transformer
from bokeh.models import Button, Div, Spinner, RangeSlider, Slider, BoxAnnotation, tools
from bokeh.layouts import layout, row
# from bokeh.models import ColumnDataSource
# from bokeh.models import GMapOptions


output_file("tile.html")

tile_provider = get_provider(CARTODBPOSITRON_RETINA)
transformer = Transformer.from_crs("epsg:4326", "epsg:3857")



# Map view-scale
width = 1_000_000

# Point coordinates
lng = 10.729437 # x
lat = 59.951812 # y

# for i in range(-180,180):
# 	print(i,transformer.transform(i,i))

# Start- and end-values for axis'
(xstart, ystart) = transformer.transform(-80, -90)
(xend, yend) = transformer.transform(85, 90)

# Point translation
(xP, yP) = transformer.transform(lat, lng)


# Defines map-view position
map = figure(
	title='See Map Here',
	x_range=(xP-width, xP+width),
	y_range=(yP-width, yP+width),
	x_axis_type="mercator",
	y_axis_type="mercator",
	tools="wheel_zoom,pan,reset"
)

# Defines map-style
map.add_tile(tile_provider)

# Adds point to map
map.circle([xP,xstart,xend], [yP,ystart,yend], size=15)

print(xP,yP)
print()
print(xstart, xend)
print(ystart, yend)
print()
print(map.x_range.start, map.x_range.end)
print(map.y_range.start, map.y_range.end)



# xrange_slider = RangeSlider(
#     title="x-axis",  # a title to display above the slider
#     start=xstart,  # set the minimum value for the slider
#     end=xend,  # set the maximum value for the slider
#     step=100,  # increments for the slider
#     value=(map.x_range.start, map.x_range.end),  # initial values for slider
# )

# yrange_slider = RangeSlider(
#     title="y-axis",  # a title to display above the slider
#     start=ystart,  # set the minimum value for the slider
#     end=yend,  # set the maximum value for the slider
#     step=100,  # increments for the slider
#     value=(map.y_range.start, map.y_range.end),  # initial values for slider
# )


# xrange_slider.js_link("value", map.x_range, "start", attr_selector=0)
# xrange_slider.js_link("value", map.x_range, "end", attr_selector=1)
# yrange_slider.js_link("value", map.y_range, "start", attr_selector=0)
# yrange_slider.js_link("value", map.y_range, "end", attr_selector=1)


# xslider = Slider(
#     title="x-pos slider",  # a title to display above the slider
#     start=xstart,  # set the minimum value for the slider
#     end=xend,  # set the maximum value for the slider
#     step=100,  # increments for the slider
#     value=(map.x_range.start, map.x_range.end),  # initial values for slider
# )

# xslider.js_link js_link("value", map.y_range, "end", attr_selector=1)




box = BoxAnnotation(left=0, right=0, bottom=0, top=0,
    fill_alpha=0.2, line_color='black', fill_color='green')

jscode = """
    box[%r] = cb_obj.start
    box[%r] = cb_obj.end
"""

xcb = CustomJS(args=dict(box=box), code=jscode % ('left', 'right'))
ycb = CustomJS(args=dict(box=box), code=jscode % ('bottom', 'top'))

map.x_range.js_on_change('start', xcb)
map.x_range.js_on_change('end', xcb)
map.y_range.js_on_change('start', ycb)
map.y_range.js_on_change('end', ycb)

mapZoom = figure(
	title='See Zoom Window Here',
	x_range=(xstart, xend),
	y_range=(ystart, yend),
	x_axis_type="mercator",
	y_axis_type="mercator",
	tools='wheel_zoom,pan,reset',
)

mapZoom.add_tile(tile_provider)
mapZoom.add_layout(box)

# source = ColumnDataSource(
# 	data=dict(
# 		lat=[*coords[1]],
# 		lon=[*coords[0]]
# 	)
# )

# print(source.data)

# map.circle(x="lon",y="lat", size=15, fill_alpha=0.6, source=source)


layout = layout([
	# [xrange_slider],
	# [yrange_slider],
	[map, mapZoom]
])

show(layout)

from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import CARTODBPOSITRON, get_provider

output_file("chicago_tile.html")
tile_provider = get_provider(CARTODBPOSITRON)

p = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000), x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

show(p)

import pandas as pd
import geopandas as gpd
import build_db
from data import dbclient
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure


def get_coles_plot():
    db = dbclient.DBClient()
    chicago = gpd.read_file('view/data/zip_shp_dir/geo_chicago.shp')
    census_table_name = build_db.CENSUS_TBL
    census_query = f"select * from {census_table_name}"
    census_df = pd.read_sql_query(census_query, db.conn)
    geo_plus_census = chicago.merge(
        census_df, left_on='zip', right_on='ZIPCODE')
    geosource = GeoJSONDataSource(geojson=geo_plus_census.to_json())
    palette = brewer['BuGn'][8]
    palette = palette[::-1]  # reverse order of colors so higher values have darker colors
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 10)
    # Define custom tick labels for color bar.
    tick_labels = {'0': '0', '1': '1',
                   '2': '2', '3': '3',
                   '4': '4', '5': '5',
                   '6': '6', '7': '7',
                   '8': '8+'}
    # Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper,
                         label_standoff=8,
                         width=500, height=20,
                         border_line_color=None,
                         location=(0, 0),
                         orientation='horizontal',
                         major_label_overrides=tick_labels)

    p = figure(title='Test Chicago Zipcode Demographics map',
               plot_height=700,  # these dimensions need some fine-tuning
               plot_width=700,
               toolbar_location='below',
               tools='pan, wheel_zoom, box_zoom, reset')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    zips = p.patches('xs', 'ys', source=geosource,
                     fill_color={'field': 'unemploy_rate',
                                 'transform': color_mapper},
                     line_color='gray',
                     line_width=0.25,
                     fill_alpha=1)
    # Create hover tool
    p.add_tools(HoverTool(renderers=[zips],
                          tooltips=[('Zipcode', '@ZIPCODE'),
                                    ('Unemploy. rate', '@unemploy_rate')]))

    return p





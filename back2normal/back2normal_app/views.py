from django.shortcuts import render, render_to_response
from plots import bokeh_test
from bokeh.embed import components


def homepage(request):
    plot = bokeh_test.get_coles_plot()
    script, div = components(plot)
    return render(request, 'base.html', {'script': script, 'div': div})

from django.shortcuts import render
from core.plots import bokeh_test
from bokeh.embed import components


def homepage(request):
    plot = bokeh_test.get_coles_plot()
    script, div = components(plot)
    return render(request, 'base.html', {'script': script, 'div': div})

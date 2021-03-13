from django.shortcuts import render
from core.plots import bokeh_test
from bokeh.embed import components


def home(request):
    # plot = bokeh_test.get_coles_plot()
    # script, div = components(plot)
    # return render(request, 'home.html', {'script': script, 'div': div})
    return render(request, 'home.html', {})

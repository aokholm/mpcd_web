from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from analyze.charthelper import chartDataJoin

import numpy as np, math
# # import matplotlib.pyplot as plt
#from prettytable import PrettyTable
#from scipy.stats import norm, chi2
#from lib.ITGrade import ITGrade as itg

#import scipy.stats as ss

#import gviz_api
from django.utils.safestring import mark_safe

# Create your views here.
def index(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/index.html', {'app_list': [app_dict],})


def design(request, app_name):
    measurements_sets = MeasurementSet.objects.all().prefetch_related('process', 'material')

    itgrades = sorted([messet.measurement_itg for messet in measurements_sets])
    input_data = itgrades
    Ndata = len(input_data)
    number = [i for i in range(1,Ndata+1)]
    cum_rank =[i*(1/float(Ndata+1)) for i in range(1, Ndata+1)]
    mean = np.mean(input_data)
    std = np.std(input_data, ddof=1)

    cum_frequency = [norm.cdf(input_data[i], loc=mean, scale=std) for i in range(Ndata)]
    cum_std = [math.sqrt(cum_frequency[i]*(1-cum_frequency[i]) / Ndata)  for i in range(Ndata)]

    t = 1.71 # for N > 10

    ll = [cum_frequency[i] - 2*cum_frequency[i] * t * cum_std[i] for i in range(Ndata)]
    ul = [cum_frequency[i] + 2*(1-cum_frequency[i]) * t * cum_std[i] for i in range(Ndata)]

    mytable = PrettyTable()

    mytable.add_column("Sortet input data", input_data)
    mytable.add_column("#number", number)
    mytable.add_column("cum_rank", cum_rank)
    mytable.add_column("cum_frequency", cum_frequency)
    mytable.add_column("cum_std", cum_std)
    mytable.add_column("lower limit", ll)
    mytable.add_column("upper limit", ul)

    # find plot range 
    plotStart   = norm.isf(0.001, loc=mean, scale=std)
    plotEnd     = norm.isf(0.999, loc=mean, scale=std)

    x = np.linspace(plotStart,plotEnd, 100).tolist()
    cdf = [norm.cdf(x[i], loc=mean, scale=std) for i in range(100)]
    cdf_std = [math.sqrt(cdf[i]*(1-cdf[i]) / Ndata)  for i in range(100)]
    cdfll = [cdf[i] - 2*cdf[i] * t * cdf_std[i] for i in range(100)]
    cdful = [cdf[i] + 2*(1-cdf[i]) * t * cdf_std[i] for i in range(100)]

    # description = [('x_value', 'number'), ('cum_rank', 'number', 'Cum. ITG.'), ('cdf', 'number'), ('cdfll', 'number'), ('cdful', 'number')]
    # chardata = chartDataJoin([input_data, x, x, x],[cum_rank, cdf, cdfll, cdful])
    

    description = [('x_value', 'number'), ('cum_rank', 'number', 'Cum. ITG.'), ('cdf', 'number'), ('cdfll', 'number'), ('cdful', 'number'), ("tooltip","String","tooltip",{"role":"tooltip"})]
    chardata = chartDataJoin([input_data, x, x, x],[cum_rank, cdf, cdfll, cdful])
    [chardata[i].append(None) for i in range(len(chardata))]

    data = chardata

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JSon string
    json = data_table.ToJSon()


    return render(request, 'analyze/design.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'itgrades' : itgrades,
            'measurement_sets': measurements_sets,
            'table' : mytable,
            'json' : mark_safe(json),

        })

def process(request, app_name):
    measurements_sets = MeasurementSet.objects.all()

    upper = 0.4
    lower = -0.4
    if request.GET.get('upper'):
        upper = float(request.GET.get('upper'))
        lower = float(request.GET.get('lower'))

    tolx = [lower, (upper+lower)/2 , upper]
    toly = [0, (upper - lower)/6, 0]

    bias = [messet.measurement_bias for messet in measurements_sets]
    dev = [messet.measurement_std for messet in measurements_sets]
    count = [messet.measurement_count for messet in measurements_sets]
    itg = [messet.measurement_itg for messet in measurements_sets]

    # Creating the data
    description = [("Bias", "number"), ("CPK =1", "number"),("Deviation","number"),("Tip","String","Tip",{"role":"tooltip"})]
    
    data = chartDataJoin([tolx, bias],[toly, dev]) 

    id_set = [messet.id for messet in measurements_sets]

    tooltip_label = [" "," "," "]
    for x in range(len(bias)):
        tooltip_label.append("Measurement set No. %s" % id_set[x])

    for x in range(len(data)):
        data[x].append(tooltip_label[x])

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JSon string
    json = data_table.ToJSon()

   
    rough_table = PrettyTable()
    
    rough_table.add_column("Id", id_set)
    rough_table.add_column("It grade", itg)
    rough_table.add_column("Bias", bias)
    rough_table.add_column("Std. Deviation", dev)
    rough_table.add_column("No. of Measurements", count)


    return render(request, 'analyze/process.html', 
        {
            'app_label': app_name,
            'view_label': 'process',
            'measurement_sets': measurements_sets,
            'json' : mark_safe(json),
            'upper' : upper,
            'lower' :lower,
            'table' : rough_table,
        })
        

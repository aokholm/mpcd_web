from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from mesdata.ITGrade import itg2tol
from analyze.charthelper import chartDataJoin

import numpy as np, math
from prettytable import PrettyTable
from scipy.stats import norm, chi2

import gviz_api
from django.utils.safestring import mark_safe

# Create your views here.
def index(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/index.html', {'app_list': [app_dict],})

def plots(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/plots.html', {'app_list': [app_dict],})



def design(request, app_name):
    measurements_sets = MeasurementSet.objects.all().prefetch_related('process', 'material')

    itgrades = sorted([messet.itg for messet in measurements_sets])

    nominalsize = ""
    if request.GET.get('nominalsize'):
        nominalsize = float(request.GET.get('nominalsize'))

    if nominalsize == "":
        micro_nomsize = 0
        input_data = itgrades
    else:
        micro_nomsize = 1
        # Change to tolerance
        input_data = []
        for x in range(len(itgrades)):
            input_data.append(itg2tol(nominalsize,itgrades[x]))
    
    
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
    
    description = {
        "x_value": ("number" , "x_value" ),
        "cum_rank": ("number" , "Cum. ITG."),
        "tooltip" : ("string","Tip1",{"role":"tooltip"}),
        "cdf" : ("number", "cdf"),
        "cdfll" : ("number", "cdfll"),
        "cdful" : ("number", "cdful")    
    }

    data = []

    for i in range(len(input_data)):
        data.append({
            "x_value": input_data[i],
            "cum_rank": cum_rank[i],
            "tooltip": ("data from No. %s" % number[i])
            })

    for i in range(len(x)):
        data.append({
            "x_value": x[i],
            "cdf": cdf[i],
            "cdfll": cdfll[i],
            "cdful": cdful[i]
            })

    #chardata = chartDataJoin([input_data, x, x, x],[cum_rank, cdf, cdfll, cdful])
    #[chardata[i].append(None) for i in range(len(chardata))]

    #data = chardata

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JSon string
    json = data_table.ToJSon(columns_order=("x_value","cum_rank","tooltip","cdf","cdfll","cdful"))

    option = {
        'title': 'Line of Best Fit(Trend Line)',
        'vAxis': {
            'title': 'Cumilative frequency',
        },
        'legend': 'none',
        'series': {
            # series 0 is the Scatter
            0: {
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            1: {
                'lineWidth': 2,
                'pointSize': 0,
                'color': 'red',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
            2: {
                'lineWidth': 1,
                'pointSize': 0,
                'color': 'blue',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
            3: {
                'lineWidth': 1,
                'pointSize': 0,
                'color': 'blue',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            }
        },
    }

    if micro_nomsize == 1:
        option.update({
            'hAxis': {
                'title': 'Symmetric tolerance [mm]'      
            }
        })
    else:
        option.update({
            'hAxis': {
                'title': 'IT grade',     
            }
        })

    return render(request, 'analyze/design.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'itgrades' : itgrades,
            'measurement_sets': measurements_sets,
            'table' : mytable,
            'json' : mark_safe(json),
            'option' : option,
            'nominalsize' : nominalsize

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
    tol_label = ["Bla1","bla2","bla3"]

    bias = [messet.mean_shift for messet in measurements_sets]
    dev = [messet.std for messet in measurements_sets]
    id_set = [messet.id for messet in measurements_sets]

    # Creating the data
    description = {
        "Bias": ("number","Bias"),
        "Cpk": ("number","Cpk =1"),
        "Cpk_tool": ("string","Tip1",{"role":"tooltip"}),
        "Deviation":("number","Measurement Sets"),
        "Deviation_tool": ("string","Tip2",{"role":"tooltip"})
    }

    data = []

    for x in range(3):
        data.append({
            "Bias":tolx[x],
            "Cpk":toly[x],
            "Cpk_tool":" "
            })

    for x in range(len(bias)):
        data.append({
            "Bias":bias[x],
            "Deviation":dev[x],
            "Deviation_tool":("Measurement set No. %s" % id_set[x])
            })

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JSon string
    json = data_table.ToJSon(columns_order=("Bias","Cpk","Cpk_tool","Deviation","Deviation_tool"))

    count = [messet.count for messet in measurements_sets]
    itg = [messet.itg for messet in measurements_sets]
   
    option = {
        'title': 'Bias vs. Deviation',
        'hAxis:': { 
            'title': 'bias'
        },
        'vAxis': {
            'title': 'Deviation',
        },
        'series': {
            0:{
                #'color': 'red', 
                'lineWidth': 2, 
                'pointSize': 0, 
                'visibleInLegend': 'true',
                'enableInteractivity': 'false',
                'tooltip':'false',
            },
            1:{
                #'color': 'blue', 
                'lineWidth': 0, 
                'pointSize': 3, 
                'visibleInLegend': 'true',
            },
        },
    }
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
            'option' : option,
        })

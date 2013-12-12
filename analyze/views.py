from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
import mesdata.PCfunctions as pc
import mesdata.PlotFunction as pf
from analyze.charthelper import chartDataJoin
from django.db.models import Q
import numpy as np, math
from prettytable import PrettyTable
from scipy.stats import norm, chi2

import gviz_api
from django.utils.safestring import mark_safe

from tags.models import GeneralTag
from numpy.numarray.alter_code1 import setshape_re

# Create your views here.
def index(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/index.html', {'app_list': [app_dict],})

def plots(request, app_name):
    measurements_sets = MeasurementSet.objects.all()

    id_set = [messet.id for messet in measurements_sets]
    itgrade = [messet.itg_pcsl for messet in measurements_sets]
    itgrade_spec = [messet.itg for messet in measurements_sets]
    cp = [messet.cp for messet in measurements_sets]

    material = [messet.material.name for messet in measurements_sets]
    specification_type = [messet.specification_type for messet in measurements_sets]


    # FIRST PLOT - ITG vs. ITG SPEC
    description1 = {
    "itgrade": ("number" , "IT Grade"),
    "itgrade_spec": ("number" , "specified IT Grade"),
    "tooltip" : ("string","Tip1",{"role":"tooltip"}),
    "xyline" : ("number", "Helper line"),
    }

    data1 =[]

    for i in range(len(id_set)):
        data1.append({
            "itgrade": itgrade[i],
            "itgrade_spec": itgrade_spec[i],
            "tooltip": ("data from No. %s" % id_set[i])
                })

    xline = [10 , 15]

    for i in range(2):
        data1.append({
            "itgrade": xline[i],
            "xyline": xline[i],
            })

    data_table1 = gviz_api.DataTable(description1)
    data_table1.LoadData(data1)

    json1 = data_table1.ToJSon(columns_order=("itgrade","itgrade_spec","tooltip","xyline"))

    option1 = {
        'title': 'Actual tolerance (IT grade) as a function of specified tolerance (IT grade)',
        'vAxis': {
            'title': 'Specified IT grade',
        },
        'hAxis': {
            'title': 'Actual IT grade',
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
        },
    }


    # SECOND PLOT - ITG ALL
    description2 = {
    "itgrade": ("number" , "cp"),
    "cum_freq": ("number" , "cumulative frequency"),
    "tooltip" : ("string","Tip1",{"role":"tooltip"}),
    "best_fit" : ("number", "best fit")
    }

    data2 =[]

    yvalue = np.linspace(0,1, len(itgrade)).tolist()
    sorted_itgrade, sorted_id = zip(*sorted(zip(itgrade,id_set)))

    for i in range(len(id_set)):
        data2.append({
            "itgrade": sorted_itgrade[i],
            "cum_freq": yvalue[i],
            "tooltip": ("data from No. %s" % sorted_id[i])
                })

    [xvalue , cdfvalue] = pc.list2cdf (itgrade)

    for i in range(len(xvalue)):
        data2.append({
            "itgrade": xvalue[i],
            "best_fit": cdfvalue[i],
            })

    data_table2 = gviz_api.DataTable(description2)
    data_table2.LoadData(data2)

    json2 = data_table2.ToJSon(columns_order=("itgrade","cum_freq","tooltip","best_fit"))

    option2 = {
        'title': 'Acumulated frequency of IT grade for all data',
        'vAxis': {
            'title': 'Probability',
        },
        'hAxis': {
            'title': 'Tolerance (IT grade)',
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
        },
    }

# Third PLOT - CP ALL
    description3 = {
    "cp": ("number" , "cp"),
    "cum_freq": ("number" , "cumulative frequency"),
    "tooltip" : ("string","Tip1",{"role":"tooltip"}),
    "best_fit" : ("number", "best fit")
    }

    data3 =[]

    yvalue = np.linspace(0,1, len(cp)).tolist()
    sorted_cp, sorted_id = zip(*sorted(zip(cp,id_set)))

    for i in range(len(id_set)):
        data3.append({
            "cp": sorted_cp[i],
            "cum_freq": yvalue[i],
            "tooltip": ("data from No. %s" % sorted_id[i])
                })

    #[xvalue , cdfvalue] = pc.list2cdf(cp)

    #    for i in range(len(xvalue)):
    #    data3.append({
    #        "cp": xvalue[i],
    #        "best_fit": cdfvalue[i],
    #        })

    data_table3 = gviz_api.DataTable(description3)
    data_table3.LoadData(data3)

    json3 = data_table3.ToJSon(columns_order=("cp","cum_freq","tooltip","best_fit"))

    option3 = {
        'title': 'Acumulated frequency of Cp for all data',
        'vAxis': {
            'title': 'Probability',
        },
        'hAxis': {
            'title': 'Cp process variance',
        },
        'legend': 'none',
        'series': {
            # series 0 is the Scatter
            0: {
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            #1: {
            #    'lineWidth': 2,
            #    'pointSize': 0,
            #    'color': 'red',
            #    'enableInteractivity': 'false',
            #    'tooltip': 'none'
            #},
        },
    }

    # Fourth plot - sorting ITG for diameter
    
    diMeasurements = MeasurementSet.objects.filter(specification_type='DI')
    notdiMeasurements = MeasurementSet.objects.filter(~Q(specification_type='DI'))
    
    lst_diameter = [messet.itg for messet in diMeasurements]
    id1 = [messet.id for messet in diMeasurements]
    lst_other = [messet.itg for messet in notdiMeasurements]
    id2 = [messet.id for messet in notdiMeasurements]

    json4 , option4= pf.lists2JsonOptions (lst_diameter,id1,lst_other,id2)

    option4.update({
        'title': 'Acumulate frequency of IT grade of diameters vs. all other data'
        })

    # fifth plot - sorting first run
    
    FirstRunGeneralTag = GeneralTag.objects.get(name = 'First run')
    
    FirstRunQuerySet = MeasurementSet.objects.filter(generaltag__in = [FirstRunGeneralTag]).distinct()
    notFirstRunQuerySet = MeasurementSet.objects.filter(~Q(generaltag__in = [FirstRunGeneralTag])).distinct()
    
    lst_firstRunItg = [sets.itg for sets in FirstRunQuerySet]
    lst_otherItg = [sets.itg for sets in notFirstRunQuerySet]
    lst_firstRunId = [sets.id for sets in FirstRunQuerySet]
    lst_otherid = [sets.id for sets in notFirstRunQuerySet]
    
    json5 , option5= pf.lists2JsonOptions (lst_firstRunItg,lst_firstRunId,lst_otherItg,lst_otherid)

    option5.update({
        'title': 'comparison of acumulated frequency of first production run vs.  all data'
        })
       
                
            
            


    return render(request, 'analyze/plots.html', 
        {
        'app_label': app_name,
        'view_label': 'lots og plot',
        'json1' : mark_safe(json1),
        'option1' : option1,
        'json2' : mark_safe(json2),
        'option2' : option2,
        'json3' : mark_safe(json3),
        'option3' : option3,
        'json4' : mark_safe(json4),
        'option4' : option4,
        'json5' : mark_safe(json5),
        'option5' : option5,
        })



def design(request, app_name):
    measurements_sets = MeasurementSet.objects.all().prefetch_related('process', 'material')

    itgrades = sorted([messet.itg_pcsl for messet in measurements_sets])

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
            input_data.append(pc.dimItg2Symtol(nominalsize,itgrades[x]))
    
    
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
    itg = [messet.itg_pcsl for messet in measurements_sets]
   
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

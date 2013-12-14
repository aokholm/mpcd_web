from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
import mesdata.PCfunctions as pc
import mesdata.PlotFunction as pf
from django.db.models import Q
import numpy as np, math
from prettytable import PrettyTable
from scipy.stats import norm
from analyze.util.plot import Plot
from analyze.util.plot_functions import list2cdf


import gviz_api
from django.utils.safestring import mark_safe

from tags.models import GeneralTag

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


    # FIRST PLOT - ITG vs. ITG SPEC
    plot1 = Plot()
    plot1.addDots(itgrade,itgrade_spec,id_set)
    plot1.addLine([8, 15],[8,15])

    # SECOND PLOT - ITG ALL
    plot2 = Plot()
    plot2.addList(itgrade,id_set)    

    # Third PLOT - CP ALL
    plot3 = Plot()
    plot3.addDots(id_set,cp,id_set)    
    
    
    # Fourth plot - sorting ITG for diameter
    
    diMeasurements = MeasurementSet.objects.filter(specification_type='DI')
    notdiMeasurements = MeasurementSet.objects.filter(~Q(specification_type='DI'))
    
    lst_diameter = [messet.itg_pcsl for messet in diMeasurements]
    id1 = [messet.id for messet in diMeasurements]
    lst_other = [messet.itg_pcsl for messet in notdiMeasurements]
    id2 = [messet.id for messet in notdiMeasurements]
    
    plot4 = Plot()
    plot4.addList(lst_diameter, id1)
    plot4.addList(lst_other, id2)

#     json4 , option4= pf.lists2JsonOptions (lst_diameter,id1,lst_other,id2)
# 
#     option4.update({
#         'title': 'Acumulate frequency of IT grade of diameters vs. all other data'
#         })
# 
#     # Method two
# #     
#     description44, data44, option44 = pf.lists2DescribtionDataOptions (lst_diameter,id1,1)
#     description45, data45, option45 = pf.lists2DescribtionDataOptions (lst_other,id2,2)
# #  
#     description44.update(description45)
#     data44.extend(data45)
#     option44['series'].update(option45['series'])
#     
#     order = tuple(description44.keys())
# 
#     data_table44 = gviz_api.DataTable(description44)
#     data_table44.LoadData(data44)
#     json44 = data_table44.ToJSon(columns_order=("xvalue","cum_freq1","tooltip1","best_fit1","cum_freq2","tooltip2","best_fit2"))

    
    # fifth plot - sorting first run
    FirstRunQuerySet = []
    notFirstRunQuerySet = []
    try:
        FirstRunGeneralTag = GeneralTag.objects.get(name = 'First run')
        FirstRunQuerySet = MeasurementSet.objects.filter(generaltag__in = [FirstRunGeneralTag]).order_by('itg_pcsl').distinct()
        notFirstRunQuerySet = MeasurementSet.objects.filter(~Q(generaltag__in = [FirstRunGeneralTag])).order_by('itg_pcsl').distinct()
    except:
        pass
    
   
    
    description5 = {
    "itg": ("number" , "IT grade"),
    "cum_freq1": ("number" , "cumulative frequency"),
    "tooltip1" : ("string","Tip1",{"role":"tooltip"}),
    "best_fit1" : ("number", "best fit"),
    "cum_freq2": ("number" , "cumulative frequency"),
    "tooltip2" : ("string","Tip2",{"role":"tooltip"}),
    "best_fit2" : ("number", "best fit")
    }

    data5 =[]
    
#     def addCumFreqValues(messets):
#         for i in range(len(messets)):
#             messets[i].cumFreq = (i+1)*(1/float(len(messets)+1))
#     
#         
#     addCumFreqValues(FirstRunQuerySet)
#     addCumFreqValues(notFirstRunQuerySet)
#     
#     
#     for i in range(len(FirstRunQuerySet)):
#         data5.append({
#             "itg": FirstRunQuerySet[i].itg_pcsl,
#             "cum_freq1": FirstRunQuerySet[i].cumFreq,
#             "tooltip1": ("data from No. %s" + str(order) )#% FirstRunQuerySet[i].id)
#                 })
#         
#     for i in range(len(notFirstRunQuerySet)):
#         data5.append({
#             "itg": notFirstRunQuerySet[i].itg_pcsl,
#             "cum_freq2": notFirstRunQuerySet[i].cumFreq,
#             "tooltip2": ("data from No. %s" % notFirstRunQuerySet[i].id)
#                 })
#        
#     [xvalue1 , cdfvalue1] = list2cdf([messet.itg_pcsl for messet in FirstRunQuerySet])
#     [xvalue2 , cdfvalue2] = list2cdf([messet.itg_pcsl for messet in notFirstRunQuerySet])
# 
#     for i in range(len(xvalue1)):
#         data5.append({
#             "itg": xvalue1[i],
#             "best_fit1": cdfvalue1[i],
#             })
# 
#     for i in range(len(xvalue2)):
#         data5.append({
#             "itg": xvalue2[i],
#             "best_fit2": cdfvalue2[i],
#             })

    data_table5 = gviz_api.DataTable(description5)
    data_table5.LoadData(data5)

    json5 = data_table5.ToJSon(columns_order=("itg","cum_freq1","tooltip1","best_fit1","cum_freq2","tooltip2","best_fit2"))

    option5 = {
        'title': 'comparison of acumulated frequency of first production run vs.  all data',
        'vAxis': {
            'title': 'Probability',
        },
        'hAxis': {
            'title': 'tolerance (IT Grade)',
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
                'color': 'blue',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
            2: {
            # you can omit this if you choose not to set any options for this series
            },
            # series 1 is the Line
            3: {
                'lineWidth': 2,
                'pointSize': 0,
                'color': 'orange',
                'enableInteractivity': 'false',
                'tooltip': 'none'
            },
        },
    }
    option5.update({
        'title': 'comparison of acumulated frequency of first production run vs.  all data'
        })
       

    return render(request, 'analyze/plots.html', 
        {
        'app_label': app_name,
        'view_label': 'lots og plot',
        'json1' : plot1.getJson(),
        'option1' : plot1.getOption(),
        'json2' : plot2.getJson(),
        'option2' : plot2.getOption(),
        'json3' : plot3.getJson(),
        'option3' : plot3.getOption(),
        'json4' : plot4.getJson(),
        'option4' : plot4.getOption(),
        'json5' : mark_safe(json5),
        'option5' : option5,
        })



def design(request, app_name):
    measurements_sets = MeasurementSet.objects.all()

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

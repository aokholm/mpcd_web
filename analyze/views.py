from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from prettytable import PrettyTable
from analyze.util.plot import Plot
from mesdata.PCfunctions import dimItg2Symtol

from django.db.models import Q
from tags.models import GeneralTag

# Create your views here.
def index(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/index.html', {'app_list': [app_dict],})

def plots(request, app_name):
    measurements_sets = MeasurementSet.objects.all().filter(ignore=False)

    id_set = [messet.id for messet in measurements_sets]
    itgrade = [messet.itg_pcsl for messet in measurements_sets]
    itgrade_spec = [messet.itg for messet in measurements_sets]
    cp = [messet.cp for messet in measurements_sets]

    # FIRST PLOT - ITG vs. ITG SPEC
    plot1 = Plot()
    plot1.addDots(itgrade,itgrade_spec,id_set)
    plot1.addLine([8, 15],[8,15])
    plot1.updateXLabel('Tolerance (IT grade)')
    plot1.updateYLabel('Specified tolerance (ITgrade)')

    # SECOND PLOT - ITG ALL
    plot2 = Plot()
    plot2.addList(itgrade,id_set)
    plot2.getValues()    

    # Third PLOT - CP ALL
    plot3 = Plot()
    plot3.addDots(id_set,cp,id_set)    
    
    
    # Fourth plot - sorting ITG for diameter
    
#     diMeasurements = MeasurementSet.objects.filter(specification_type='DI')
#     notdiMeasurements = MeasurementSet.objects.filter(~Q(specification_type='DI'))
#     
#     lst_diameter = [messet.itg_pcsl for messet in diMeasurements]
#     id1 = [messet.id for messet in diMeasurements]
#     lst_other = [messet.itg_pcsl for messet in notdiMeasurements]
#     id2 = [messet.id for messet in notdiMeasurements]
#     
#     plot4 = Plot()
#     plot4.addList(lst_diameter, id1)
#     plot4.addList(lst_other, id2)


    
    # fifth plot - sorting first run
#     FirstRunQuerySet = []
#     notFirstRunQuerySet = []
#     try:
#         FirstRunGeneralTag = GeneralTag.objects.get(name = 'First run')
#         FirstRunQuerySet = MeasurementSet.objects.filter(generaltag__in = [FirstRunGeneralTag]).order_by('itg_pcsl').distinct()
#         notFirstRunQuerySet = MeasurementSet.objects.filter(~Q(generaltag__in = [FirstRunGeneralTag])).order_by('itg_pcsl').distinct()
#     except:
#         pass
     
    

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
#         'json4' : plot4.getJson(),
#         'option4' : plot4.getOption(),
#         'json5' : mark_safe(json5),
#         'option5' : option5,
        })




def process(request, app_name):
    
    measurements_sets = MeasurementSet.objects.all().filter(ignore=False)

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
    count = [messet.count for messet in measurements_sets]
    itg = [messet.itg_pcsl for messet in measurements_sets]

    plot1 = Plot()
    plot1.addDots(bias, dev, id_set)
    plot1.addLine(tolx, toly)
    plot1.updateXLabel('bias')
    plot1.updateYLabel('deviation')
    plot1.updateTitle('Bias vs. Deviation')
      
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
            'json' : plot1.getJson(),
            'option' : plot1.getOption(),
            'upper' : upper,
            'lower' :lower,
            'table' : rough_table,
        })

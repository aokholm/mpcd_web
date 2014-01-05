from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from prettytable import PrettyTable
from analyze.util.plot import Plot
from analyze.util.plot import createStardardPlots
from analyze.util.messetContainer import MessetContainer

from django.db.models import Q
from tags.models import GeneralTag

# Create your views here.
def index(request, app_name):
    app_dict = {
        'name': app_name,
    }

    return render(request, 'analyze/index.html', {'app_list': [app_dict],})

def plots(request, app_name):
    
    MSetBase = MeasurementSet.objects.all().filter(ignore=False)
    
    plots = []
    
    messets = [
              MessetContainer(MSetBase.filter(measurement_report__manufacturer__name='Simo-tek'), title='Simo-tek'),
              MessetContainer(MSetBase.filter(~Q(measurement_report__manufacturer__name='Simo-tek')), title='Other')
              ]
    
    plots.extend(createStardardPlots(messets))
    
    
    # MOULD HALF
    MSGTacross = GeneralTag.objects.get(name = 'across mould halfs')
    MSGTInternal = GeneralTag.objects.get(name = 'Internal in mold half')
    
    messets = [
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTacross]).distinct(), title='Internal mould measurement'),
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTInternal]).distinct(), title='Across mould half measurement'),
               ]
    
    plots.extend(createStardardPlots(messets))
    
#     plot = Plot()
#     plot.setXAxis('itg_pcsl')
#     plot.addMessets(messets)
#     plot.updateTitle('Comparison of measurements internal in mould and across mould halfs')
#     plot.updateXLabel('Tolerance (IT grade)')
#     plot.updateYLabel('Probability')
#     plots.append(plot) 
    
    
    # Sorting ITG for diameter
    messets = [
               MessetContainer(MSetBase.filter(Q(specification_type='R') | Q(specification_type='D')), title='Diameters and Radius'),
               MessetContainer(MSetBase.filter(Q(specification_type='Di')), title='Linear')
               ]
    
    plots.extend(createStardardPlots(messets))
#     plot = Plot()
#     plot.setXAxis('itg_pcsl')
#     plot.addMessets(messets)
#     plot.updateTitle('Comparison of linear measurements and diameter and radius')
#     plot.updateXLabel('Tolerance (IT grade)')
#     plot.updateYLabel('Probability')   
#     plots.append(plot) 
    
    
    # Inside Outside 
    MSGTinside = GeneralTag.objects.get(name = 'Inside(Hole)')
    MSGToutside = GeneralTag.objects.get(name = 'outside(shaft)')
    
    messets = [
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTinside]).distinct(), title='Inside(hole)'),
               MessetContainer(MSetBase.filter(generaltag__in = [MSGToutside]).distinct(), title='Outside(shaft)'),
               ]
    plots.extend(createStardardPlots(messets))
    
#     plot = Plot()
#     plot.setXAxis('itg_pcsl')
#     plot.addMessets(messets)
#     plot.updateTitle('Comparison of measurements inside and outside geometries')
#     plot.updateXLabel('Tolerance (IT grade)')
#     plot.updateYLabel('Probability')   
#     plots.append(plot) 
    
    
    # Diameters or radius
    messets = [
               MessetContainer(MSetBase.filter(target__lt=3), title='small (x < 3)'),
               MessetContainer(MSetBase.filter(target__gte=3).filter(target__lt=6), title='medium (3 <= x < 6)'),
               MessetContainer(MSetBase.filter(target__gte=6), title='large (6 <= x)'),
            ]
    plots.extend(createStardardPlots(messets))
    
#     plot = Plot()
#     plot.setXAxis('itg_pcsl')
#     plot.addMessets(messets)
#     plot.updateTitle('Comparison of capability of sizes')
#     plot.updateXLabel('Tolerance (IT grade)')
#     plot.updateYLabel('Probability')
#     plots.append(plot)    
    
    
    
#     diMeasurements = MeasurementSet.objects.filter(specification_type='DI')
#     notdiMeasurements = MeasurementSet.objects.filter(~Q(specification_type='DI'))

    
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
        'plots' : plots,
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

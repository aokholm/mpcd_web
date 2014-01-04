from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from prettytable import PrettyTable
from analyze.util.plot import Plot
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
    measurement_sets1 = MeasurementSet.objects.all().filter(ignore=False).filter(measurement_report__manufacturer__name='Simo-tek')
    measurement_sets2 = MeasurementSet.objects.all().filter(ignore=False).filter(~Q(measurement_report__manufacturer__name='Simo-tek'))
    
    messet1 = MessetContainer(measurement_sets1, title='Simo-tek')
    messet2 = MessetContainer(measurement_sets2, title='Other')

    plots = []

    # ITG vs. ITG SPEC
    plot = Plot()
    plot.setXAxis('itg')
    plot.setYAxis('itg_pcsl')
    plot.addMessets([messet1, messet2])
    plot.addLine([8, 15],[8,15])
    plot.updateXLabel('Specified tolerance (ITgrade)')
    plot.updateYLabel('Tolerance (IT grade)')
    plot.updateTitle('Specified vs Actual Tolerances')
    
    plots.append(plot)
    
    # ITG ALL
    plot = Plot()
    plot.setXAxis('itg_pcsl') 
    plot.addMessets([messet1, messet2])
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')
    plot.updateTitle('Capability of manufactoring companies')
    plots.append(plot)
    
    # MOULD HALF
    MSGTacross = GeneralTag.objects.get(name = 'across mould halfs')
    MSGTInternal = GeneralTag.objects.get(name = 'Internal in mold half')
    
    measurement_sets3 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTacross]).distinct()
    measurement_sets4 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTInternal]).distinct()
    
    messet3 = MessetContainer(measurement_sets3, title='Internal mould measurement')
    messet4 = MessetContainer(measurement_sets4, title='Across mould half measurement')
    
    plot = Plot()
    plot.setXAxis('itg_pcsl')
    plot.addMessets([messet3, messet4])
    plot.updateTitle('Comparison of measurements internal in mould and across mould halfs')
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')
    plots.append(plot) 
    
    # Sorting ITG for diameter
    measurement_sets5 = MeasurementSet.objects.all().filter(ignore=False).filter(Q(specification_type='R') | Q(specification_type='D')) 
    measurement_sets6 = MeasurementSet.objects.all().filter(ignore=False).filter(Q(specification_type='Di'))
    
    messet5 = MessetContainer(measurement_sets5, title='Diameters and Radius')
    messet6 = MessetContainer(measurement_sets6, title='Linear')
    
    plot = Plot()
    plot.setXAxis('itg_pcsl')
    plot.addMessets([messet5, messet6])
    plot.updateTitle('Comparison of linear measurements and diameter and radius')
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')   
    plots.append(plot) 
    
    
    # Sorting 
    MSGTinside = GeneralTag.objects.get(name = 'Inside(Hole)')
    MSGToutside = GeneralTag.objects.get(name = 'outside(shaft)')
    
    measurement_sets7 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTinside]).distinct()
    measurement_sets8 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGToutside]).distinct()
    
    messet7 = MessetContainer(measurement_sets7, title='Inside(hole)')
    messet8 = MessetContainer(measurement_sets8, title='Outside(shaft)')
    
    plot = Plot()
    plot.setXAxis('itg_pcsl')
    plot.addMessets([messet7, messet8])
    plot.updateTitle('Comparison of measurements inside and outside geometries')
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')   
    plots.append(plot) 
    
    
    # Diameters or radius
    measurement_sets1 = MeasurementSet.objects.filter(ignore=False).filter(target__lt=3)
    measurement_sets2 = MeasurementSet.objects.filter(ignore=False).filter(target__gte=3).filter(target__lt=6)
    measurement_sets3 = MeasurementSet.objects.filter(ignore=False).filter(target__gte=6)
    
    messets = [
               MessetContainer(measurement_sets1, title='small (x < 3)'),
               MessetContainer(measurement_sets2, title='medium (3 <= x < 6)'),
               MessetContainer(measurement_sets3, title='large (6 <= x)'),
            ]
    
    plot = Plot()
    plot.setXAxis('itg_pcsl')
    plot.addMessets(messets)
    plot.updateTitle('Comparison of capability of sizes')
    plot.updateXLabel('Tolerance (IT grade)')
    plot.updateYLabel('Probability')
    plots.append(plot)    
    
    
    
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

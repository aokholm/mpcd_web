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
    
    measurement_sets1.legend = 'Simo-Tek'

    # FIRST PLOT - ITG vs. ITG SPEC
    plot1 = Plot()
    plot1.setXAxis('itg')
    plot1.setYAxis('itg_pcsl')
    plot1.addMessets([messet1, messet2])
    plot1.addLine([8, 15],[8,15])
    plot1.updateXLabel('Specified tolerance (ITgrade)')
    plot1.updateYLabel('Tolerance (IT grade)')
    plot1.updateTitle('Specified vs Actual Tolerances')

    # SECOND PLOT - ITG ALL
    plot2 = Plot()
    plot2.setXAxis('itg_pcsl') 
    plot2.addMessets([messet1, messet2])
    plot2.updateXLabel('Tolerance (IT grade)')
    plot2.updateYLabel('Probability')
    plot2.updateTitle('Capability of manufactoring companies')
    
    # Third PLOT
    MSGTacross = GeneralTag.objects.get(name = 'across mould halfs')
    MSGTInternal = GeneralTag.objects.get(name = 'Internal in mold half')
    
    measurement_sets3 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTacross]).distinct()
    measurement_sets4 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTInternal]).distinct()
    
    messet3 = MessetContainer(measurement_sets3, title='Internal mould measurement')
    messet4 = MessetContainer(measurement_sets4, title='Across mould half measurement')
    
    plot3 = Plot()
    plot3.setXAxis('itg_pcsl')
    plot3.addMessets([messet3, messet4])
    plot3.updateTitle('Comparison of measurements internal in mould and across mould halfs')
    plot3.updateXLabel('Tolerance (IT grade)')
    plot3.updateYLabel('Probability')   
    
    # Fourth plot - sorting ITG for diameter
    measurement_sets5 = measurement_sets1.filter(Q(specification_type='R') | Q(specification_type='D')) 
    measurement_sets6 = measurement_sets2.filter(Q(specification_type='Di'))
    
    messet5 = MessetContainer(measurement_sets5, title='Diameters and Radius')
    messet6 = MessetContainer(measurement_sets6, title='Linear')
    
    plot4 = Plot()
    plot4.setXAxis('itg_pcsl')
    plot4.addMessets([messet5, messet6])
    plot4.updateTitle('Comparison of linear measurements and diameter and radius')
    plot4.updateXLabel('Tolerance (IT grade)')
    plot4.updateYLabel('Probability')   
    
    # Fifth plot - sorting 
    MSGTinside = GeneralTag.objects.get(name = 'Inside(Hole)')
    MSGToutside = GeneralTag.objects.get(name = 'outside(shaft)')
    
    measurement_sets7 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGTinside]).distinct()
    measurement_sets8 = MeasurementSet.objects.filter(ignore=False).filter(generaltag__in = [MSGToutside]).distinct()
    
    messet7 = MessetContainer(measurement_sets7, title='Inside(hole)')
    messet8 = MessetContainer(measurement_sets8, title='Outside(shaft)')
    
    plot5 = Plot()
    plot5.setXAxis('itg_pcsl')
    plot5.addMessets([messet7, messet8])
    plot5.updateTitle('Comparison of measurements inside and outside geometries')
    plot5.updateXLabel('Tolerance (IT grade)')
    plot5.updateYLabel('Probability')   
    
    # Diameters or radius
    measurement_sets9 = MeasurementSet.objects.filter(ignore=False)
    
    messet9 = MessetContainer(measurement_sets9, title='small (< 3mm)')
    
    plot6 = Plot()
    plot6.setXAxis('itg_pcsl')
    plot6.addMessets([messet9])
    plot6.updateTitle('Comparison of capability of sizes')
    plot6.updateXLabel('Tolerance (IT grade)')
    plot6.updateYLabel('Probability')     
    
    plot7 = Plot()
    plot8 = Plot()

    
    
    
    
    
    
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
        'json4' : plot4.getJson(),
        'option4' : plot4.getOption(),
        'json5' : plot5.getJson(),
        'option5' : plot5.getOption(),
        'json6' : plot6.getJson(),
        'option6' : plot6.getOption(),
        'json7' : plot7.getJson(),
        'option7' : plot7.getOption(),
        'json8' : plot8.getJson(),
        'option8' : plot8.getOption(),
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

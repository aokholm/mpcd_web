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
    MSetBase = MSetBase.filter(Q(specification_type='R') | Q(specification_type='D') | Q(specification_type='Di') | Q(specification_type='PT'))
    MSetBase = MSetBase.select_related('measurement_report')
    plots = []
    
    messets = [
              MessetContainer(MSetBase.filter(measurement_report__manufacturer__name='Simo-tek'), title='Manufactured by Simo-tek'),
              MessetContainer(MSetBase.filter(~Q(measurement_report__manufacturer__name='Simo-tek')), title='Other')
              ]
    
    plots.extend(createStardardPlots(messets))
    
    
    # MOULD HALF
    MSGTacross = GeneralTag.objects.get(name = 'across mould halfs')
    MSGTInternal = GeneralTag.objects.get(name = 'Internal in mold half')
    MSGTBoth = GeneralTag.objects.get(name = 'in both mould halfs')
    MSGTSplitline = GeneralTag.objects.get(name = 'part of splitline')
    
    messets = [
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTacross]).distinct(), title='Across mould half measurement'),
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTInternal]).distinct(), title='Internal mould measurement'),
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTBoth]).distinct(), title='Measurement in both mould halfs'),
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTSplitline]).distinct(), title='Measurement part of split line'),
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
    
    # Functional vs non-functional
    MSGTFunctional = GeneralTag.objects.get(name = 'Functional dimension')    
    messets = [
               MessetContainer(MSetBase.filter(generaltag__in = [MSGTFunctional]).distinct(), title='Functional surface'),
               MessetContainer(MSetBase.filter(~Q(generaltag__in = [MSGTFunctional])).distinct(), title='Non critical surface')
               ]
    plots.extend(createStardardPlots(messets))
    
        # Functional vs non-functional
    MSGTException = GeneralTag.objects.get(name = 'exeception attributes')
    MSGTException_children = MSGTException.get_children()
    MSGTExceptionList = [MSGTException_child.pk for MSGTException_child in MSGTException_children]
    MSGTExceptionList.append(MSGTException.pk)
    
    messets = [ 
               MessetContainer(MSetBase.filter(generaltag__in = MSGTExceptionList).distinct(), title='Exceptions'),
               MessetContainer(MSetBase.filter(~Q(generaltag__in = MSGTExceptionList)).distinct(), title='Other')
               ]
    plots.extend(createStardardPlots(messets))
    
    
    
    # Measurement companies
    messets = [
              MessetContainer(MSetBase.filter(measurement_report__measurementCompany__name='Simo-tek').filter(Q(measurement_report__part_name__contains ='Rotor') | Q(measurement_report__part_name__contains ='Axel')), title='Measured by Simo-tek'),
              MessetContainer(MSetBase.filter(~Q(measurement_report__measurementCompany__name='Simo-tek')).filter(Q(measurement_report__part_name__contains ='Rotor') | Q(measurement_report__part_name__contains ='Axel')), title='Other')
              ]
    plots.extend(createStardardPlots(messets))
    
    
    # DEESIGN EXAMPLE
    # Measurement companies
    # MSGTFunctional
    # MSGTInternal
    # MSGTinside
    # MSGToutside
    # Q(specification_type='D')
    
    messets = [
              MessetContainer(MSetBase.filter(specification_type='D').filter(generaltag__in = [MSGTInternal] ).filter(generaltag__in = [MSGTinside] ).distinct(), title='Int, Inside'),
              MessetContainer(MSetBase.filter(specification_type='D').filter(generaltag__in = [MSGTacross, MSGTBoth] ).filter(generaltag__in = [MSGToutside] ).distinct(), title='Across, Outside'),
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

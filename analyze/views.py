from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mesdata.models import MeasurementSet
from prettytable import PrettyTable
from analyze.util.plot import Plot

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
    
    ids1 = [messet.id for messet in measurement_sets1]
    itgrades1 = [messet.itg_pcsl for messet in measurement_sets1]
    itgrade_specs1 = [messet.itg for messet in measurement_sets1]
     
     
    ids2 = [messet.id for messet in measurement_sets2]
    itgrades2 = [messet.itg_pcsl for messet in measurement_sets2]
    itgrade_specs2 = [messet.itg for messet in measurement_sets2]
    

    # FIRST PLOT - ITG vs. ITG SPEC
    plot1 = Plot()
    plot1.addDots(itgrade_specs1, itgrades1, ids1, legend='Simo-tek')
    plot1.addDots(itgrade_specs2, itgrades2, ids2, legend='Other')
    plot1.addLine([8, 15],[8,15])
    plot1.updateXLabel('Specified tolerance (ITgrade)')
    plot1.updateYLabel('Tolerance (IT grade)')
    plot1.updateTitle('Specified vs Actual Tolerances')

    # SECOND PLOT - ITG ALL
    plot2 = Plot()
    plot2.addList(itgrades2,ids2)
    plot2.addList(itgrades1,ids1)
    plot2.updateXLabel('Tolerance (IT grade)')
    plot2.updateYLabel('Probability')
    plot2.getValues()    

    # Third PLOT - CP ALL
    cps = [messet.cp for messet in measurement_sets1]
    cp = [messet.cp for messet in measurement_sets2]
    
    plot3 = Plot()
    plot3.addDots(ids2,cp,ids2)
    plot3.addDots(ids1,cps,ids1)    
    
    # Fourth plot - sorting ITG for diameter
    cbs = [messet.cb for messet in measurement_sets1]
    cb = [messet.cb for messet in measurement_sets2]
    
    plot4 = Plot()
    plot4.addList(cb, ids2)
    plot4.addList(cbs, ids1)
    plot4.updateXLabel('Cb normalised mean shift')
    
    # Fifth plot - sorting 
    
    DI_sel_sets =  measurement_sets1.filter(specification_type='DI')
    DI_mea_sets =  measurement_sets2.filter(specification_type='DI')
    
    DI_itgs = [messet.itg_pcsl for messet in DI_sel_sets]
    DI_itg = [messet.itg_pcsl for messet in DI_mea_sets]
    DI_ids = [messet.id for messet in DI_sel_sets]
    DI_id = [messet.id for messet in DI_mea_sets]
    
    plot5 = Plot()
    plot5.addList(DI_itg,DI_id)
    plot5.addList(DI_itgs, DI_ids)
    plot5.updateTitle('For Linear measurements only')
    
    # Diameters or radius
    
    DR_sel_sets = measurement_sets1.filter(Q(specification_type='R') | Q(specification_type='D')) 
    DR_mea_sets = measurement_sets2.filter(Q(specification_type='R') | Q(specification_type='D'))
    
    DR_itgs = [messet.itg_pcsl for messet in DR_sel_sets]
    DR_itg = [messet.itg_pcsl for messet in DR_mea_sets]
    DR_cbs = [messet.cb for messet in DR_sel_sets]
    DR_cb = [messet.cb for messet in DR_mea_sets]
    DR_ids = [messet.id for messet in DR_sel_sets]
    DR_id = [messet.id for messet in DR_mea_sets]
    
    
    plot6 = Plot()
    plot6.addList(DR_itg, DR_id)
    plot6.addList(DR_itgs, DR_ids)
    plot6.updateTitle('Diameters and radius')
    
    
    plot7 = Plot()
    plot7.addList(DR_cb, DR_id)
    plot7.addList(DR_cbs, DR_ids)
    plot7.updateXLabel('CB')
    
    # inside outside
     
    in_sel_sets = []
    in_mea_sets = []
    out_sel_sets = []
    out_mea_sets = []
    
    try:
        inside_GT = GeneralTag.objects.get(pk = 5)
#         in_sel_sets = measurement_sets1.filter(generaltag__in = [inside_GT]).distinct()
        in_mea_sets = measurement_sets2.filter(generaltag__in = [inside_GT]).distinct()
        outside_GT = GeneralTag.objects.get(name = 'outside(shaft)')
#         out_sel_sets = measurement_sets1.filter(generaltag__in = [outside_GT]).distinct()
        out_mea_sets = measurement_sets2.filter(generaltag__in = [outside_GT]).distinct()
    except:
        pass
    
#     in_cbs = [messet.cb for messet in in_sel_sets]
    in_cb = [messet.cb for messet in in_mea_sets]
#     in_ids = [messet.id for messet in in_sel_sets]
    in_id = [messet.id for messet in in_mea_sets]
    
    plot8 = Plot()
    plot8.addList(in_cb, in_id)
#     plot8.addList(in_cbs, in_ids)
    plot8.updateXLabel('CB')
    
    
    
    
    
    
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

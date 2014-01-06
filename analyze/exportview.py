'''
Created on Jan 6, 2014

@author: aokholmRetina
'''

from mesdata.models import MeasurementSet
from django.shortcuts import render


def export(request, app_name):
    
    data = [['MN', 'MR', 'T', 'N', 'MU', 'B', 'STD', 'ST', 'TYPE', 'I', 'TAG']]
    
    messets = MeasurementSet.objects.all().select_related('measurement_report').prefetch_related('generaltag')
    for messet in messets:
        GTlist.append(messet.generaltag.all())
    
    
    
    
    return render(request, 'analyze/export.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'data': data,
            'gtList': GTlist,

        })
'''
Created on Jan 6, 2014

@author: aokholmRetina
'''

from prettytable import PrettyTable
from mesdata.models import MeasurementSet
from django.shortcuts import render


def export(request, app_name):
    
    data = []
    data.append(['MR', 'MN', 'T', 'ST', 'N', 'MU', 'STD', 'TYPE', 'I', 'TAG'])
#     prettyData = PrettyTable(['MR', 'MN', 'T', 'ST', 'N', 'MU', 'STD', 'TYPE', 'I', 'TAG'])
    #x.align["City name"] = "l" # Left align city names
#     prettyData.padding_width = 1 # One space between column edges and contents (default)
    
    conv = {
            'hard' : 'HTM',
            'long' : 'LS',
            'Func' : 'FUNC',
            'Insi' : 'IN',
            'outs' : 'OUT',
            'acro' : 'ACM',
            'in b' : 'INBM',
            'Inte' : 'INTM',
            'part' : 'SPLM',
                   }
    
    def findAltName(input):
        if input in conv:
            out = conv[input]
        else:
            out = input
        return out
        
        
    
    messets = MeasurementSet.objects.all().select_related('measurement_report').prefetch_related('generaltag')
    for messet in messets:
        
        tags = messet.generaltag.all()
        shortTags = [findAltName(tag.name[:4]) for tag in tags]
        
        
        tagString = ','.join(shortTags)
        
        
        if messet.mean:
            mean = '{:03.3f}'.format(float(messet.mean))
        else:
            mean = messet.mean
        
        if messet.std:
            std = '{:.3e}'.format(float(messet.std))
        else:
            std = messet.std
        
        if messet.ignore:
            ignore = 'T'
        else:
            ignore = 'F'
        
        row = [
            messet.measurement_report.part_name,
            messet.measurement_number,
            '{:03.3f}'.format(float(messet.target)),
            messet.symtol,
            messet.count,
            mean ,
            std,
            messet.specification_type,
            ignore,
            tagString,
            ]
        
        data.append(row)
#         prettyData.add_row(row)
        
#         prettyString = prettyData.get_string(border=False)

    return render(request, 'analyze/export.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'data' : data,
        })
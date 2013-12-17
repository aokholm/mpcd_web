'''
Created on Dec 17, 2013

@author: aokholmRetina
'''
from mesdata.models import MeasurementSet
from mesdata.PCfunctions import dimItg2Symtol
from django.shortcuts import render
from analyze.util.plot import Plot
from django import forms
from django.db.models import Q



class DesignForm(forms.Form):
    specification_type = forms.ChoiceField(choices=MeasurementSet.SPECTYPE_CHOICES, required=False)


def design(request, app_name):
    
    if request.method == 'POST': # If the form has been submitted...
        form = DesignForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.cleaned_data['specification_type'] 
    else:
        form = DesignForm() # An unbound form
        
    
    measurements_sets = MeasurementSet.objects.all().filter(ignore=False).filter(Q(specification_type='R') | Q(specification_type='D'))

    itgrade =[messet.itg_pcsl for messet in measurements_sets]
    id_set =  [messet.id for messet in measurements_sets]
            
    nominalsize = ""
    if request.GET.get('nominalsize'):
        nominalsize = float(request.GET.get('nominalsize'))

    if nominalsize == "":
        micro_nomsize = 0
        input_data = itgrade
    else:
        micro_nomsize = 1
        # Change to tolerance
        input_data = []
        for x in range(len(itgrade)):
            input_data.append(dimItg2Symtol(nominalsize,itgrade[x]))
    
    plot1 = Plot()
    plot1.addList(input_data,id_set)
    plot1.addConfidenceInterval(input_data)
    
    if micro_nomsize:
        plot1.updateXLabel('Tolerance (mm)')
    

    return render(request, 'analyze/design.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'measurement_sets': measurements_sets,
            'json' : plot1.getJson(),
            'option' : plot1.getOption(),
            'nominalsize' : nominalsize,
            'form': form,

        })

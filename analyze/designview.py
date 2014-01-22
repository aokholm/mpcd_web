'''
Created on Dec 17, 2013

@author: aokholmRetina
'''
from mesdata.models import MeasurementSet, MeasurementReport, Manufacturer, MeasurementCompany
from django.shortcuts import render
from analyze.util.plot import Plot
from analyze.util.plot import createStardardPlots
from django import forms
from django.db.models import Q
from tags.models import GeneralTag, MeasurementReportTag
from analyze.util.messetContainer import MessetContainer



class DesignForm(forms.Form):
    specification_type = forms.MultipleChoiceField(choices=MeasurementSet.SPECTYPE_CHOICES[:4], required=False)
    measurement_report = forms.ModelMultipleChoiceField(queryset=MeasurementReport.objects.all(), required=False)
    general_tag = forms.ModelMultipleChoiceField(queryset=GeneralTag.objects.all(), required=False)
    manufacturer = forms.ModelMultipleChoiceField(queryset=Manufacturer.objects.all(), required=False)
    measurement_company = forms.ModelMultipleChoiceField(queryset=MeasurementCompany.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super (DesignForm, self).__init__(*args, **kwargs)
        self.fields['specification_type'].widget.attrs['class'] = "halfHeight"
        
        

def design(request, app_name):
    
    if request.method == 'POST': # If the form has been submitted...
        form = DesignForm(request.POST) # A form bound to the POST data
        
    else:
        form = DesignForm() # An unbound form
    
    
    MSetBase = MeasurementSet.objects.all().filter(ignore=False)
    MSetBase = MSetBase.filter(Q(specification_type='R') | Q(specification_type='D') | Q(specification_type='Di') | Q(specification_type='PT'))
    MSetBase = MSetBase.select_related('measurement_report')
    plots = []
    
    messet1 = MSetBase;
    
    if form.is_valid(): # All validation rules pass
        # Process the data in form.cleaned_data
        # ...
        if form.cleaned_data['specification_type']:
            messet1 = messet1.filter(specification_type__in = form.cleaned_data['specification_type'])
            
        if form.cleaned_data['measurement_report']:
            messet1 = messet1.filter(measurement_report__in = form.cleaned_data['measurement_report'])
            
        if form.cleaned_data['general_tag']:
            messet1 = messet1.filter(generaltag__in = form.cleaned_data['general_tag'])
            
        if form.cleaned_data['manufacturer']:
            messet1 = messet1.filter(measurement_report__manufacturer__in = form.cleaned_data['manufacturer'])
            
        if form.cleaned_data['measurement_company']:
            messet1 = messet1.filter(measurement_report__measurementCompany__in = form.cleaned_data['measurement_company'])
    
    messets = [
               MessetContainer(messet1, '1'),
              ]
    
    plots.extend(createStardardPlots(messets))
#     if micro_nomsize:
#         plot1.updateXLabel('Tolerance (mm)')
    

    return render(request, 'analyze/design.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'plots' : plots,
            'form': form,
            'measurement_sets': messets,
        })

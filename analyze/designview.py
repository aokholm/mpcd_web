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
from analyze.util.PCData import PCData
from django.forms.formsets import formset_factory
from mesdata.PCfunctions import ninety, dimItg2Symtol


class DesignForm(forms.Form):
    nominel        = forms.DecimalField(min_value=2, max_value=500, required=False)

class DesignFormSet(forms.Form):
    specification_type      = forms.MultipleChoiceField(choices=MeasurementSet.SPECTYPE_CHOICES[:4], required=False)
    measurement_report      = forms.ModelMultipleChoiceField(queryset=MeasurementReport.objects.all(), required=False)
    general_tag             = forms.ModelMultipleChoiceField(queryset=GeneralTag.objects.all(), required=False)
    manufacturer            = forms.ModelMultipleChoiceField(queryset=Manufacturer.objects.all(), required=False)
    measurement_company     = forms.ModelMultipleChoiceField(queryset=MeasurementCompany.objects.all(), required=False)
    
    
    def __init__(self, *args, **kwargs):
        super (DesignFormSet, self).__init__(*args, **kwargs)
        self.fields['specification_type'].widget.attrs['class'] = "halfHeight"
        self.fields['manufacturer'].widget.attrs['class'] = "quaterHeight"
        self.fields['measurement_company'].widget.attrs['class'] = "quaterHeight"      

def design(request, app_name):
    
    DesignFormSets = formset_factory(DesignFormSet)
    
    
    MSetBase = MeasurementSet.objects.all().filter(ignore=False)
    MSetBase = MSetBase.filter(Q(specification_type='R') | Q(specification_type='D') | Q(specification_type='Di') | Q(specification_type='PT'))
    MSetBase = MSetBase.select_related('measurement_report')
    plots = []
    
    messets = []
    PCDatas = []
    Names = ['Left', 'Right']
    messetNr = 0;
    
    if request.method == 'POST': # If the form has been submitted...
        formset = DesignFormSets(request.POST)
        designform = DesignForm(request.POST)
        if formset.is_valid() and designform.is_valid():
    # do something with the formset.cleaned_data
            for form in formset.forms: 
                messet = MSetBase
                # Process the data in form.cleaned_data
                # ...
                
                if form.cleaned_data: #because no fields are required
                    
                    if form.cleaned_data['specification_type']:
                        messet = messet.filter(specification_type__in = form.cleaned_data['specification_type'])
                        
                    if form.cleaned_data['measurement_report']:
                        messet = messet.filter(measurement_report__in = form.cleaned_data['measurement_report'])
                        
                    if form.cleaned_data['general_tag']:
                        messet = messet.filter(generaltag__in = form.cleaned_data['general_tag'])
                        
                    if form.cleaned_data['manufacturer']:
                        messet = messet.filter(measurement_report__manufacturer__in = form.cleaned_data['manufacturer'])
                        
                    if form.cleaned_data['measurement_company']:
                        messet = messet.filter(measurement_report__measurementCompany__in = form.cleaned_data['measurement_company'])
                    
                messets.append(MessetContainer(messet, Names[messetNr]))
                messetNr = messetNr + 1
            
            nominel = designform.cleaned_data['nominel']
            
            messetNr = 0
            for messet in messets:
                pcData = PCData()
                
                xvals = [getattr(measurementSet, 'itg_pcsl') for measurementSet in messet.measurementSets]
                pcData.Title = Names[messetNr]
                pcData.ITG_90 = ninety(xvals)
                if nominel:
                    pcData.PCSL = dimItg2Symtol(float(nominel), pcData.ITG_90)
                else:
                    pcData.PCSL = ''
                
                PCDatas.append(pcData)
                messetNr = messetNr + 1
        
    else:
        designform = DesignForm() # An unbound form
        formset = formset_factory(DesignFormSet, extra=2)
        messets.append(MessetContainer(MSetBase, Names[messetNr]))
        messetNr = messetNr + 1
    
    
    
    plots.extend(createStardardPlots(messets))
#     if micro_nomsize:
#         plot1.updateXLabel('Tolerance (mm)')
    

    return render(request, 'analyze/design.html', 
        {
            'app_label': app_name,
            'view_label': 'design',
            'plots' : plots,
            'designform' : designform,
            'formset': formset,
            'measurement_sets': messets,
            'PCDatas' : PCDatas,
        })

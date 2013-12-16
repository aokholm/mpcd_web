from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django import forms
from mesdata.models import MeasurementReport, Measurement, MeasurementSet
from tags.models import MeasurementEquipment
import csv

class BatchImportForm(forms.Form):
    mesdataCSV = forms.CharField(widget=forms.Textarea)
    measurement_report = forms.ModelChoiceField(MeasurementReport.objects.all(), empty_label=None)
    measurement_equipment = forms.ModelChoiceField(MeasurementEquipment.objects.all(), empty_label="(Nothing)", required=False)


app_name = "dataimport"


def batch(request):
    
    measurementsetsRAW = None
    
    if request.method == 'POST': # If the form has been submitted...
        form = BatchImportForm(request.POST) # A form bound to the POST data
                
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            passedmesdataCSV = csv.reader(form.cleaned_data['mesdataCSV'].splitlines(), delimiter='\t')
            
            measurementsetsRAW = zip(*passedmesdataCSV) # ('1a', '2.9401944', '2.9407817', '2.9513863',...)
            
            for measurementsetRaw in measurementsetsRAW:
                measurement_number = measurementsetRaw[0] # get measurement number
                target = float(measurementsetRaw[1]) # target value
                
                if measurementsetRaw[2] != '': # Lower specification limit
                    lsl = float(measurementsetRaw[2])
                else:
                    lsl = None
                    
                if measurementsetRaw[3] != '':
                    usl = float(measurementsetRaw[3]) # Upper specification limit
                else:
                    usl = None
                
                if measurementsetRaw[4] != '':
                    specification_type = measurementsetRaw[4]
                else:
                    specification_type = None
                
                actual_sizes = measurementsetRaw[5:]
                try:
                    firstEmptyStringIndex = actual_sizes.index('')
                    actual_sizes = actual_sizes[:firstEmptyStringIndex]
                except :
                    pass
                
                actual_sizes = [float(x) for x in actual_sizes]

                measurementset = MeasurementSet()
                measurementset.measurement_number = measurement_number
                measurementset.measurement_report = form.cleaned_data['measurement_report']
                measurementset.target = target
                measurementset.lsl = lsl
                measurementset.usl = usl
                measurementset.specification_type = specification_type
                
                if form.cleaned_data['measurement_equipment'] != None:
                    measurementset.measurement_equipment = form.cleaned_data['measurement_equipment']
                
                measurementset.save()
                
                measurementList = []
                
                for actual_size in actual_sizes:
                    measurement = Measurement()
                    measurement.actual_size = actual_size
                    measurement.measurement_set = measurementset
                    measurementList.append(measurement)
                
                Measurement.objects.bulk_create(measurementList)
                
                measurementset.save()
                
                
        return HttpResponseRedirect('thanks/') # Redirect after POST
    else:
        form = BatchImportForm() # An unbound form
        
    return render(request, 'dataimport/batch.html', {
        'form': form,
        'passedmesdataCSV' : measurementsetsRAW,
    })



# Create your views here.

def thanks(request):
    html = "awesome data uploaded"
    return HttpResponse(html)


def index(request):
    html = "<html><body>Simpel %s.</body></html>" % app_name
    return HttpResponse(html)

# def index(request, app_name):
#     app_dict = {
#         'name': app_name,
#     }
# 
#     return render(request, 'analyze/index.html', {'app_list': [app_dict],})
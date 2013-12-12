from django.contrib import admin
from mesdata.models import Measurement
from mesdata.PCfunctions import stdMeanshiftCpk2Symtol, UslLsl2SymTol, c4stdCorrectionFactor, dimSymtol2Itg
from numpy import mean, std

# admin MEASUREMENT
class MeasurementInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Measurement
    extra = 10

class MeasurementSetAdmin(admin.ModelAdmin):
    raw_id_fields = ('material','process','generaltag','equipment',)

    autocomplete_lookup_fields = {
        'fk' : ['material', 'process', 'equipment'],
        'm2m' : ['generaltag'],
    }

    readonly_fields = ('id','ca', 'ca_pcsl', 'cb', 'cp', 'itg', 'itg_pcsl')
    list_display = ('id','count','itg','target','pub_date',)
    search_fields = ['id','material__name', 'process__name', 'generaltag__name', 'equipment__name']
    list_filter = ['pub_date', ]

    fieldsets = [
        (None,   {
            'classes': ('grp-collapse grp-open',),
            'fields': ['target','material','process','equipment','generaltag','specification_type','usl','lsl','pub_date' ]
        }),
        ('Additional information', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['price','weight','manufac','measured','machine','pro_yield']
        }),
        ('Process capability information', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['ca','ca_pcsl','cb','cp','itg','itg_pcsl']
        }),
    ]
    inlines = (MeasurementInline, )

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(MeasurementSetAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(MeasurementSetAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        measurements = [x.actual_size for x in obj.measurements.all()]
        
        obj.count = len(measurements)
        obj.cpk = 1.66
        obj.mean_shift = obj.target - mean(measurements)
        obj.std = std(measurements, ddof=1)/c4stdCorrectionFactor(obj.count)
        
        obj.pcsl = stdMeanshiftCpk2Symtol(obj.std, obj.mean_shift, obj.cpk)
        obj.symtol = UslLsl2SymTol( obj.usl, obj.lsl)
        
        obj.itg = dimSymtol2Itg(obj.target, obj.symtol)
        obj.itg_pcsl = dimSymtol2Itg(obj.target, obj.pcsl)
      
        obj.ca = 1 - abs(obj.mean_shift) / obj.symtol
        obj.ca_pcsl = 1-abs(obj.mean_shift)/ obj.pcsl
        obj.cb = obj.mean_shift / obj.symtol
        obj.cp = obj.symtol / (3 * obj.std)

        obj.save()
        return obj
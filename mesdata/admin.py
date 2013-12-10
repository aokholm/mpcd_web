from django.contrib import admin
from mesdata.models import Measurement, MeasurementSet
from mesdata.ITGrade import stdbias2itg
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

    readonly_fields = ('id','ca', 'ca_pcsl', 'cb', 'cp', 'itg', 'itg_spec')
    list_display = ('id','count','itg','nominal_size','pub_date',)
    search_fields = ['id','material__name', 'process__name', 'generaltag__name', 'equipment__name']
    list_filter = ['pub_date', ]

    fieldsets = [
        (None,   {
            'classes': ('grp-collapse grp-open',),
            'fields': ['nominal_size','material','process','equipment','generaltag','specification_type','tol_up','tol_low','pub_date' ]
        }),
        ('Additional information', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['price','weight','manufac','measured','machine','pro_yield']
        }),
        ('Process capability information', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['ca','ca_pcsl','cb','cp','itg','itg_spec']
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
        nominal_size = obj.nominal_size

        obj.cpk = 1.66
        obj.mean_shift = nominal_size - mean(measurements)
        obj.std = std(measurements) # Should implement correction factor
        obj.itg = stdbias2itg(nominal_size, obj.std, obj.mean_shift, obj.cpk)
        obj.save()
        return obj
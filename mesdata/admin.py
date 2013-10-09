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

    readonly_fields = ('id',)
    list_display = ('id','measurement_count','measurement_itg','nominal_size','pub_date',)

    fieldsets = [
        (None,   {
            'classes': ('grp-collapse grp-open',),
            'fields': ['nominal_size','material','process','equipment','generaltag','measurement_type','tol_up','tol_low','pub_date' ]
        }),
        ('Confidential information', {
            'classes': ('grp-collapse grp-open',),
            'fields': ['price','weight','manufac','measured','machine','pro_yield']
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
        obj.measurement_count = len(measurements)
        nominal_size = obj.nominal_size

        obj.measurement_cpk = 1.33
        obj.measurement_bias = nominal_size - mean(measurements)
        obj.measurement_std = std(measurements)
        obj.measurement_itg = stdbias2itg(nominal_size, obj.measurement_std, obj.measurement_bias, obj.measurement_cpk,)
        obj.save()
        return obj
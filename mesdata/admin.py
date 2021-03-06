from django.contrib import admin
from mesdata.models import Measurement, Manufacturer, MeasurementCompany, MeasurementReport,\
    MeasurementSet

# admin MEASUREMENT
class MeasurementInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Measurement
    extra = 10
    
class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    
class MeasurementCompanyAdmin(admin.ModelAdmin):
    model = MeasurementCompany

class MeasurementSetInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = MeasurementSet
    extra = 0
    fields = ('measurement_number', 'ignore', 'measurement_equipment', 'generaltag', 'specification_type')
    
class MeasurementReportAdmin(admin.ModelAdmin):
    inlines = (MeasurementSetInline, )

class MeasurementSetAdmin(admin.ModelAdmin):
#     raw_id_fields = ('generaltag','measurement_equipment',)

#     autocomplete_lookup_fields = {
#         'fk' : ['measurement_equipment'],
#         'm2m' : ['generaltag'],
#     }

    readonly_fields = ('id','mean', 'std', 'cpk', 'pcsl', 'ca', 'ca_pcsl', 'cb', 'cp', 'itg', 'itg_pcsl')
    list_display = ('id', 'measurement_report', 'measurement_number', 'target', 'count','specification_type',)
    search_fields = ['id','measurement_report__material__name', 'measurement_report__process__name', 'generaltag__name',]
    list_filter = ['measurement_report', ]

    fieldsets = [
        (None,   {
            'classes': ('grp-collapse grp-open',),
            'fields': ['measurement_report', 'measurement_number', 'measurement_equipment','generaltag', 'specification_type','target', 'usl','lsl']
        }),
        ('Process capability information', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ['mean', 'std', 'pcsl', 'cpk', 'ca', 'ca_pcsl', 'cb', 'cp', 'itg','itg_pcsl']
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
        obj.save()
        return obj
from django.contrib import admin
from mesdata.models import Measurement, Manufacturer, MeasurementCompany, MeasurementReport

# admin MEASUREMENT
class MeasurementInline(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    model = Measurement
    extra = 10
    
class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    
class MeasurementCompanyAdmin(admin.ModelAdmin):
    model = MeasurementCompany

class MeasurementSetAdmin(admin.ModelAdmin):
    raw_id_fields = ('generaltag','measurement_equipment',)

    autocomplete_lookup_fields = {
        'fk' : ['measurement_equipment'],
        'm2m' : ['generaltag'],
    }

    readonly_fields = ('id','ca', 'ca_pcsl', 'cb', 'cp', 'itg', 'itg_pcsl')
    list_display = ('id', 'measurement_report', 'measurement_number', 'target', 'count','specification_type')
    search_fields = ['id','measurement_report__material__name', 'measurement_report__process__name', 'generaltag__name', 'equipment__name']
    list_filter = [ ]

    fieldsets = [
        (None,   {
            'classes': ('grp-collapse grp-open',),
            'fields': ['measurement_report', 'measurement_number', 'measurement_equipment','generaltag','specification_type','target', 'usl','lsl']
        }),
#         ('Additional information', {
#             'classes': ('grp-collapse grp-open',),
#             'fields': ['price','weight','manufac','measured','machine','pro_yield']
#         }),
        ('Process capability information', {
            'classes': ('grp-collapse grp-closed',),
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
        obj.save()
        return obj
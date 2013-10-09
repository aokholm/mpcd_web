from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from tags.models import ProcessAlternativeName, MaterialAlternativeName
#from tags.models import 

## admin TAGS
class AlternativeProcessAdmin(admin.TabularInline):
    model = ProcessAlternativeName

class AlternativeMaterialAdmin(admin.TabularInline):
    model = MaterialAlternativeName

class MaterialAdmin(MPTTModelAdmin):
    list_display = ['name', 'alternative_names_']
    search_fields = ['name', 'material_names__name',]

    def queryset(self, request):
        return super(MaterialAdmin, self).queryset(request).prefetch_related('material_names')

    inlines = [AlternativeMaterialAdmin,]

class ProcessAdmin(MPTTModelAdmin):
    list_display = ['name', 'alternative_names_',]
    search_fields = ['name', 'process_names__name',]

    def queryset(self, request):
        return super(ProcessAdmin, self).queryset(request).prefetch_related('process_names')

    inlines = [AlternativeProcessAdmin,]

class GeneralTagAdmin(MPTTModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]

class MeasurementEquipmentAdmin(MPTTModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]


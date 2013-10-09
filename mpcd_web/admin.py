from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.http import HttpResponse

#from mesdata.models import Measurement, MeasurementSet
#from mesdata.admin import MeasurementSetAdmin
from tags.models import *
from tags.admin import *

from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

class MyAdminSite(admin.AdminSite):

    index_template = 'admin/index_mod.html'

    def get_urls(self):
        urls = super(MyAdminSite, self).get_urls()

        my_urls = patterns('',
            url(r'^(?P<app_name>analyze)/', include('analyze.urls', namespace="analyze")),
        )
        return my_urls + urls

        
admin_site = MyAdminSite('myadmin')  

#admin_site.register(MeasurementSet,MeasurementSetAdmin)


#admin_site.register(MaterialAlternativeName)
admin_site.register(Material, MaterialAdmin)
#admin_site.register(ProcessAlternativeName)
admin_site.register(Process, ProcessAdmin)
admin_site.register(GeneralTag, GeneralTagAdmin)
admin_site.register(MeasurementEquipment, GeneralTagAdmin)


admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)




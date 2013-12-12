'''
Created on Dec 12, 2013

@author: aokholmRetina
'''

from django.core.management.base import BaseCommand, CommandError
from mesdata.models import MeasurementSet
from tags.models import GeneralTag

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        self.stdout.write('Succesfully run script')
    
        distMeasurementSets = MeasurementSet.objects.filter(specification_type = "D")
        
        for distMesset in distMeasurementSets:
            print str(distMesset.id) + " " + distMesset.specification_type
#
                
        innerGT = GeneralTag.objects.get(name = "Inner")
        
        innerMessets = MeasurementSet.objects.filter(generaltag__in = [innerGT]).distinct()
        
        for xMessets in innerMessets:
            for gt in xMessets.generaltag.all():
                print str(xMessets.id) + " " + gt.name
# 
#     def handle(self, *args, **options):
#         for poll_id in args:
#             try:
#                 poll = Poll.objects.get(pk=int(poll_id))
#             except Poll.DoesNotExist:
#                 raise CommandError('Poll "%s" does not exist' % poll_id)
# 
#             poll.opened = False
#             poll.save()
# 
#             self.stdout.write('Successfully closed poll "%s"' % poll_id)
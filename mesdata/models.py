from django.db import models
from datetime import datetime    
from django import forms

# Create your models here.
class Measurement(models.Model):
    """ The Measured data for a simple component """
    actual_size = models.FloatField('Actual size') 
    measurement_set = models.ForeignKey('MeasurementSet', related_name='measurements')


    def __unicode__(self):
        return str(self.actual_size)

class MeasurementSet(models.Model):
    count = models.IntegerField('No. Measurements',blank=True, default=0)
    mean = models.FloatField('Mean', blank=True, null=True)
    mean_shift = models.FloatField('Mean Shift', blank=True, null=True)
    std = models.FloatField('Standard deviation',blank=True, null=True)
    
    ca = models.FloatField('Process Centering', blank=True, null=True, editable=False)
    ca_pcsl = models.FloatField('Process Cent. PCSL', blank=True, null=True)
    cb = models.FloatField('Normalized Bias', blank=True, null=True)
    cp = models.FloatField('Process Variation', blank=True, null=True)
    itg = models.FloatField('PCSL (IT grade)', blank=True, null=True)
    itg_spec = models.FloatField('Spec. IT grade', blank = True, null = True)
    
    nominal_size = models.FloatField('Nominal Size', blank=True, null=True)
    tol_up = models.FloatField('Upper tolerance',blank=True, null=True) 
    tol_low = models.FloatField('Lower tolerance',blank=True, null=True)

    price = models.FloatField('Price per 1000 [$]',blank=True, null=True) 
    weight = models.FloatField('Weight of product [kg]',blank=True, null=True)
    manufac = models.CharField('Manufacturer',max_length=200,blank=True, null=True)
    measured = models.CharField('Measured by whom',max_length=200,blank=True, null=True)
    machine = models.CharField('Which Machine',max_length=200,blank=True, null=True)
    pro_yield = models.CharField('Production yield',max_length=200,blank=True, null=True)
    pub_date = models.DateTimeField('Date Published',default=datetime.now, blank=False)

    material = models.ForeignKey('tags.Material', related_name='measurement_sets')
    material.allow_tags = True
    process = models.ForeignKey('tags.Process',related_name='measurement_sets')
    generaltag = models.ManyToManyField('tags.GeneralTag',verbose_name='General Tag',related_name='measurement_sets',blank=True,null=True)
    equipment = models.ForeignKey('tags.MeasurementEquipment',related_name='measurement_sets')


    RADIUS = 'R'
    DIAMETER = 'D'
    NONGPS_DISTANCE = 'DI'
    NONGPS_ANGLE = 'A'

    STRAIGHTNESS = 'S'
    PLANARITY = 'P'
    CIRCULARITY = 'CI'
    CYLINDRICITY = 'CY'    
    PROFILE_OF_LINE = 'PL'
    PROFILE_OF_SURFACE = 'PS'
    PERPENDICULARITY = 'PE'    
    ANGULARITY = 'AN'
    PARALLELISM = 'P'
    SYMMETRY = 'SY'
    POSITIONAL_TOLERANCE = 'PT'
    CONCENTRICITY = 'CO'
    CIRCULAR_RUNOUT = 'CR'
    TOTAL_RUNOUT = 'TR'
    OTHER = 'O'

    SPECTYPE_CHOICES = (
        (RADIUS, 'Radius'),
        (DIAMETER, 'Diameter') ,
        (NONGPS_DISTANCE, 'Distance (non GPS)'),
        (NONGPS_ANGLE, 'Angle (non GPS)'),
        (STRAIGHTNESS, 'Straightness'),
        (PLANARITY, 'Planarity'),
        (CIRCULARITY, 'Circularity'),
        (CYLINDRICITY, 'Cylindricity'),
        (PROFILE_OF_LINE, 'Profile of Line' ),
        (PROFILE_OF_SURFACE, 'Profile of Surface'),
        (PERPENDICULARITY, 'Perpendicularity'),
        (ANGULARITY, 'Angularity'),
        (PARALLELISM, 'Parallelism'),
        (SYMMETRY, 'Symetry'),
        (POSITIONAL_TOLERANCE, 'Positional Tolerance'),
        (CONCENTRICITY, 'Concetricity'),
        (CIRCULAR_RUNOUT, 'Circular Runout'),
        (TOTAL_RUNOUT, 'Total Runout'),
        (OTHER, 'Other'),
    )

    specification_type = models.CharField(max_length=2, choices=SPECTYPE_CHOICES, default='O')

    def __unicode__(self):
        return """Measurement Set %s""" % (self.id)
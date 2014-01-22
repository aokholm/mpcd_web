from datetime import datetime
from django.db import models
from mesdata.PCfunctions import stdMeanshiftCpk2Symtol, UslLsl2SymTol, c4stdCorrectionFactor, dimSymtol2Itg
from numpy import mean, std

# Create your models here.
class Measurement(models.Model):
    """ The Measured data for a simple component """
    actual_size = models.FloatField('Actual size') 
    measurement_set = models.ForeignKey('MeasurementSet', related_name='measurements')


    def __unicode__(self):
        return str(self.actual_size)

class MeasurementCompany(models.Model):
    name = models.CharField(max_length=60, unique=True)
    
    COUNTRY_CHOICES = (
            ('DK', 'Denmark'),
            ('CH', 'China'),)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='DK')
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "process_names__name__icontains"
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=60, unique=True)
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "process_names__name__icontains"
    

class MeasurementReport(models.Model):
    part_name = models.CharField('Part Name', max_length=60)
    drawingKey = models.CharField('Drawing Key', max_length = 60, unique=True, blank = True, null= True)
    
    material = models.ForeignKey('tags.Material', related_name='measurement_reports')
    material.allow_tags = True
    process = models.ForeignKey('tags.Process',related_name='measurement_reports')
    tags = models.ManyToManyField('tags.MeasurementReportTag', related_name='measurement_reports',blank=True,null=True)
    
    manufacturer = models.ForeignKey('mesdata.Manufacturer', related_name='measurement_sets', blank=True,null=True)
    measurementCompany = models.ForeignKey('mesdata.MeasurementCompany', related_name='measurement_sets', blank=True,null=True)
    
    machine = models.CharField('Machine Code',max_length=200,blank=True, null=True)
    
    part_yield = models.CharField('Part yield',max_length=200,blank=True, null=True)
    pub_date = models.DateTimeField('Date Published',default=datetime.now, blank=False)
    price = models.FloatField('Price per 1000 [$]',blank=True, null=True) 
    weight = models.FloatField('Weight of product [kg]',blank=True, null=True)
    
    def __unicode__(self):
        return self.part_name + ' ' + self.drawingKey


class MeasurementSet(models.Model):
    measurement_number = models.CharField(max_length=24)
    count = models.IntegerField('No. Measurements',blank=True, default=0)
    mean = models.FloatField('Mean', blank=True, null=True)
    mean_shift = models.FloatField('Mean Shift', blank=True, null=True)
    std = models.FloatField('Standard deviation',blank=True, null=True)
    
    pcsl = models.FloatField('PCSL', blank=True, null=True)
    ca = models.FloatField('Process Centering (Ca)', blank=True, null=True)
    ca_pcsl = models.FloatField('Process Cent. PCSL (Ca_pcsl)', blank=True, null=True)
    cb = models.FloatField('Normalized Bias (Cb)', blank=True, null=True)
    cp = models.FloatField('Process Variation (Cp)', blank=True, null=True)
    cpk = models.FloatField('Cpk', blank=True, null=True)
    itg = models.FloatField('IT grade (ITG)', blank = True, null = True)
    itg_pcsl = models.FloatField('IT grade (ITG_pcsl)', blank=True, null=True)
    
    target = models.FloatField('Nominal / Target')
    usl = models.FloatField('Upper tolerance',blank=True, null=True)
    lsl = models.FloatField('Lower tolerance',blank=True, null=True)
    symtol = models.FloatField('Symmetric tolerance', blank=True, null=True)
    
    ignore = models.BooleanField('Ignore Measurement', default=False)

    measurement_report = models.ForeignKey('mesdata.MeasurementReport', related_name='measurement_sets')
    generaltag = models.ManyToManyField('tags.GeneralTag',verbose_name='General Tag',related_name='measurement_sets',blank=True,null=True)
    measurement_equipment = models.ForeignKey('tags.MeasurementEquipment',  related_name='measurement_sets',blank=True,null=True)
    

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
    
    def setPCparameters(self):
        measurements = [x.actual_size for x in self.measurements.all()]
        if len(measurements) >= 2:
            self.count = len(measurements)
            self.mean = mean(measurements)
    
            self.cpkDesired = 1.66
            self.mean_shift = self.mean - self.target
            self.std = std(measurements, ddof=1)/c4stdCorrectionFactor(self.count)
            
            self.pcsl = stdMeanshiftCpk2Symtol(self.std, self.mean_shift, self.cpkDesired)
            self.ca_pcsl = 1-abs(self.mean_shift)/ self.pcsl
            self.itg_pcsl = dimSymtol2Itg(self.target, self.pcsl)
            
            if (self.usl != None and self.lsl != None):
                self.symtol = UslLsl2SymTol( self.usl, self.lsl)
                self.itg = dimSymtol2Itg(self.target, self.symtol)
                self.ca = 1 - abs(self.mean_shift) / self.symtol
                self.cb = self.mean_shift / self.symtol
                self.cp = self.symtol / (3 * self.std)
                m = (self.lsl + self.usl) / 2
                self.cpk = ( self.symtol - abs(self.mean - m) ) / (3*self.std) 
    
    def save(self, *args, **kwargs):
        self.setPCparameters()
        super(MeasurementSet, self).save(*args, **kwargs) # Call the "real" save() method.
    
    
        
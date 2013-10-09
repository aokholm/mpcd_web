from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from string import join
from django.contrib import admin
from mptt.admin import MPTTModelAdmin


## Models
class MaterialAlternativeName(models.Model):
    name = models.CharField(max_length=60, unique=True)
    material_node = models.ForeignKey('Material', related_name='material_names')

    def __unicode__(self):
        return self.name

class ProcessAlternativeName(models.Model):
    name = models.CharField(max_length=60, unique=True)
    process_node = models.ForeignKey('Process', related_name='process_names')

    def __unicode__(self):
        return self.name

class Material(MPTTModel):
    name = models.CharField(max_length=60, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name

    def alternative_names_(self):
        lst = [x.name for x in self.material_names.all()]
        return str(join(lst, ', '))

    class MPTTMeta:
        order_insertion_by = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "material_names__name__icontains",  "parent__name__icontains"

    def related_label(self):
        indents = '-' * self.level
        indent_string = ' '.join(indents)
        children = (self.rght - self.lft-1)/2
        if children:
            children = u" - %s submaterials" % (children)
        else:
            children = ""

        alternative_names = self.alternative_names_()
        if alternative_names == "":
            alternative_names = ""
        else:
            alternative_names = u" | %s" % alternative_names

        return u"%s %s%s%s" % (indent_string, self.name, children, alternative_names)
        # indent_px = self.level * 10 + 5
        # return u"<p style='padding-left: %spx;'>%s (%s)</p>" % (indent_px, self.name, self.alternative_names_())


class Process(MPTTModel):
    name = models.CharField(max_length=60, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name

    def alternative_names_(self):
        lst = [x.name for x in self.process_names.all()]
        return str(join(lst, ', '))

    class MPTTMeta:
        order_insertion_by = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "process_names__name__icontains"

    def related_label(self):
        indents = '-' * self.level
        indent_string = ' '.join(indents)
        children = (self.rght - self.lft-1)/2
        if children:
            children = u" - %s subprocesses" % (children)
        else:
            children = ""

        alternative_names = self.alternative_names_()
        if alternative_names == "":
            alternative_names = ""
        else:
            alternative_names = u" | %s" % alternative_names

        return u"%s %s%s%s" % (indent_string, self.name, children, alternative_names)


class GeneralTag(MPTTModel):
    name = models.CharField(max_length=60, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "process_names__name__icontains"

    def related_label(self):
        indents = '-' * self.level
        indent_string = ' '.join(indents)
        children = (self.rght - self.lft-1)/2
        if children:
            children = u" - %s sub tags" % (children)
        else:
            children = ""

        return u"%s %s%s" % (indent_string, self.name, children)

class MeasurementEquipment(MPTTModel):
    name = models.CharField(max_length=60, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", ) # "process_names__name__icontains"

    def related_label(self):
        indents = '-' * self.level
        indent_string = ' '.join(indents)
        children = (self.rght - self.lft-1)/2
        if children:
            children = u" - %s submeasurement-equipment " % (children)
        else:
            children = ""

        return u"%s %s%s" % (indent_string, self.name, children)
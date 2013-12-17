# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field generaltag on 'MeasurementReport'
        db.delete_table(db.shorten_name(u'mesdata_measurementreport_generaltag'))


    def backwards(self, orm):
        # Adding M2M table for field generaltag on 'MeasurementReport'
        m2m_table_name = db.shorten_name(u'mesdata_measurementreport_generaltag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measurementreport', models.ForeignKey(orm[u'mesdata.measurementreport'], null=False)),
            ('generaltag', models.ForeignKey(orm[u'tags.generaltag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['measurementreport_id', 'generaltag_id'])


    models = {
        u'mesdata.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        u'mesdata.measurement': {
            'Meta': {'object_name': 'Measurement'},
            'actual_size': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'measurements'", 'to': u"orm['mesdata.MeasurementSet']"})
        },
        u'mesdata.measurementcompany': {
            'Meta': {'object_name': 'MeasurementCompany'},
            'country': ('django.db.models.fields.CharField', [], {'default': "'DK'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        u'mesdata.measurementreport': {
            'Meta': {'object_name': 'MeasurementReport'},
            'drawingKey': ('django.db.models.fields.CharField', [], {'max_length': '60', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'measurement_sets'", 'null': 'True', 'to': u"orm['mesdata.Manufacturer']"}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'measurement_reports'", 'to': u"orm['tags.Material']"}),
            'measurementCompany': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'measurement_sets'", 'null': 'True', 'to': u"orm['mesdata.MeasurementCompany']"}),
            'part_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'part_yield': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'measurement_reports'", 'to': u"orm['tags.Process']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'measurement_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tags.MeasurementReportTag']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'mesdata.measurementset': {
            'Meta': {'object_name': 'MeasurementSet'},
            'ca': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ca_pcsl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'cb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'cp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'generaltag': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'measurement_sets'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['tags.GeneralTag']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'itg_pcsl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lsl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mean_shift': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'measurement_equipment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'measurement_sets'", 'null': 'True', 'to': u"orm['tags.MeasurementEquipment']"}),
            'measurement_number': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'measurement_report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'measurement_sets'", 'to': u"orm['mesdata.MeasurementReport']"}),
            'pcsl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'specification_type': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '2'}),
            'std': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'symtol': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.FloatField', [], {}),
            'usl': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tags.generaltag': {
            'Meta': {'object_name': 'GeneralTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.GeneralTag']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'tags.material': {
            'Meta': {'object_name': 'Material'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.Material']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'tags.measurementequipment': {
            'Meta': {'object_name': 'MeasurementEquipment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.MeasurementEquipment']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'tags.measurementreporttag': {
            'Meta': {'object_name': 'MeasurementReportTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.MeasurementReportTag']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'tags.process': {
            'Meta': {'object_name': 'Process'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['tags.Process']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['mesdata']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Timezones'
        db.create_table(u'zonesapp_timezones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timezone_name', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('offset', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('local_time', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'zonesapp', ['Timezones'])

        # Adding model 'UserEntry'
        db.create_table(u'zonesapp_userentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry_name', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('city_name', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('gmt_offset_display', self.gf('django.db.models.fields.TimeField')(default='00:00:00')),
        ))
        db.send_create_signal(u'zonesapp', ['UserEntry'])

        # Adding M2M table for field tmz on 'UserEntry'
        m2m_table_name = db.shorten_name(u'zonesapp_userentry_tmz')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userentry', models.ForeignKey(orm[u'zonesapp.userentry'], null=False)),
            ('timezones', models.ForeignKey(orm[u'zonesapp.timezones'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userentry_id', 'timezones_id'])


    def backwards(self, orm):
        # Deleting model 'Timezones'
        db.delete_table(u'zonesapp_timezones')

        # Deleting model 'UserEntry'
        db.delete_table(u'zonesapp_userentry')

        # Removing M2M table for field tmz on 'UserEntry'
        db.delete_table(db.shorten_name(u'zonesapp_userentry_tmz'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'zonesapp.timezones': {
            'Meta': {'object_name': 'Timezones'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'local_time': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'offset': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'timezone_name': ('django.db.models.fields.TextField', [], {'max_length': '500'})
        },
        u'zonesapp.userentry': {
            'Meta': {'object_name': 'UserEntry'},
            'city_name': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'entry_name': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'gmt_offset_display': ('django.db.models.fields.TimeField', [], {'default': "'00:00:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tmz': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['zonesapp.Timezones']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['zonesapp']
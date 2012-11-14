# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('dalliz_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Cart'], null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
        ))
        db.send_create_signal('dalliz', ['User'])

        # Adding model 'Cart_content'
        db.create_table('dalliz_cart_content', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Cart'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dalliz.Product'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('dalliz', ['Cart_content'])

        # Adding unique constraint on 'Cart_content', fields ['cart', 'product']
        db.create_unique('dalliz_cart_content', ['cart_id', 'product_id'])

        # Adding model 'Cart'
        db.create_table('dalliz_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
        ))
        db.send_create_signal('dalliz', ['Cart'])


    def backwards(self, orm):
        # Removing unique constraint on 'Cart_content', fields ['cart', 'product']
        db.delete_unique('dalliz_cart_content', ['cart_id', 'product_id'])

        # Deleting model 'User'
        db.delete_table('dalliz_user')

        # Deleting model 'Cart_content'
        db.delete_table('dalliz_cart_content')

        # Deleting model 'Cart'
        db.delete_table('dalliz_cart')


    models = {
        'dalliz.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'dalliz.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dalliz.Product']", 'through': "orm['dalliz.Cart_content']", 'symmetrical': 'False'}),
            'session_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'})
        },
        'dalliz.cart_content': {
            'Meta': {'unique_together': "(('cart', 'product'),)", 'object_name': 'Cart_content'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dalliz.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'dalliz.category_sub': {
            'Meta': {'object_name': 'Category_sub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Category_main']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'dalliz.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dalliz.Category_sub']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9999'})
        },
        'dalliz.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'dalliz.user': {
            'Meta': {'object_name': 'User'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Cart']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'})
        }
    }

    complete_apps = ['dalliz']
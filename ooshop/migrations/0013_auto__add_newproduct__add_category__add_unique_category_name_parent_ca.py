# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewProduct'
        db.create_table('ooshop_newproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewBrand'], null=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Unit'], null=True)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('goodie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('origine', self.gf('django.db.models.fields.TextField')(null=True)),
            ('informations', self.gf('django.db.models.fields.TextField')(null=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(null=True)),
            ('conservation', self.gf('django.db.models.fields.TextField')(null=True)),
            ('conseils', self.gf('django.db.models.fields.TextField')(null=True)),
            ('composition', self.gf('django.db.models.fields.TextField')(null=True)),
            ('avertissements', self.gf('django.db.models.fields.TextField')(null=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=9999999999999999999999L)),
            ('package_quantity', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('package_measure', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('package_unit', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('ooshop', ['NewProduct'])

        # Adding M2M table for field categories on 'NewProduct'
        db.create_table('ooshop_newproduct_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newproduct', models.ForeignKey(orm['ooshop.newproduct'], null=False)),
            ('category', models.ForeignKey(orm['ooshop.category'], null=False))
        ))
        db.create_unique('ooshop_newproduct_categories', ['newproduct_id', 'category_id'])

        # Adding model 'Category'
        db.create_table('ooshop_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.Category'], null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=9999, unique=True, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('ooshop', ['Category'])

        # Adding unique constraint on 'Category', fields ['name', 'parent_category']
        db.create_unique('ooshop_category', ['name', 'parent_category_id'])

        # Adding model 'NewBrand'
        db.create_table('ooshop_newbrand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
        ))
        db.send_create_signal('ooshop', ['NewBrand'])

        # Adding model 'History'
        db.create_table('ooshop_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.NewProduct'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('shipping_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.ShippingArea'], null=True)),
            ('availability', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=9999999999999999999999L)),
        ))
        db.send_create_signal('ooshop', ['History'])

        # Adding model 'ShippingArea'
        db.create_table('ooshop_shippingarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.TextField')(null=True)),
            ('postal_code', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_shipping_area', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ooshop', ['ShippingArea'])

        # Adding model 'Promotion'
        db.create_table('ooshop_promotion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='s', max_length=1)),
            ('image_url', self.gf('django.db.models.fields.CharField')(max_length=9999, null=True)),
            ('before', self.gf('django.db.models.fields.FloatField')()),
            ('after', self.gf('django.db.models.fields.FloatField')()),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('shipping_area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ooshop.ShippingArea'], null=True)),
        ))
        db.send_create_signal('ooshop', ['Promotion'])

        # Adding M2M table for field content on 'Promotion'
        db.create_table('ooshop_promotion_content', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('promotion', models.ForeignKey(orm['ooshop.promotion'], null=False)),
            ('newproduct', models.ForeignKey(orm['ooshop.newproduct'], null=False))
        ))
        db.create_unique('ooshop_promotion_content', ['promotion_id', 'newproduct_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['name', 'parent_category']
        db.delete_unique('ooshop_category', ['name', 'parent_category_id'])

        # Deleting model 'NewProduct'
        db.delete_table('ooshop_newproduct')

        # Removing M2M table for field categories on 'NewProduct'
        db.delete_table('ooshop_newproduct_categories')

        # Deleting model 'Category'
        db.delete_table('ooshop_category')

        # Deleting model 'NewBrand'
        db.delete_table('ooshop_newbrand')

        # Deleting model 'History'
        db.delete_table('ooshop_history')

        # Deleting model 'ShippingArea'
        db.delete_table('ooshop_shippingarea')

        # Deleting model 'Promotion'
        db.delete_table('ooshop_promotion')

        # Removing M2M table for field content on 'Promotion'
        db.delete_table('ooshop_promotion_content')


    models = {
        'dalliz.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
        'monoprix.brand': {
            'Meta': {'object_name': 'Brand'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'monoprix.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_sub_level_2']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_sub_level_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_1'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.category_sub_level_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_2'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Category_sub_level_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'monoprix.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Brand']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['monoprix.Category_final']", 'symmetrical': 'False'}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseil': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'dalliz_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Product']", 'null': 'True'}),
            'dalliz_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'promotion': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9999'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monoprix.Unit']"}),
            'unit_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'valeur_nutritionnelle': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'monoprix.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'monoprix_unit_dalliz_unit'", 'symmetrical': 'False', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'ooshop.brand': {
            'Meta': {'object_name': 'Brand'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_brand_dalliz_brand'", 'null': 'True', 'to': "orm['dalliz.Brand']"}),
            'dalliz_brand_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_brand_dalliz_brand_M2M'", 'symmetrical': 'False', 'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ooshop.brand_matching': {
            'Meta': {'object_name': 'Brand_matching'},
            'dalliz_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dalliz.Brand']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ooshop_brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Brand']"}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.category': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'})
        },
        'ooshop.category_final': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_final'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'dalliz_category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_category_final_category_dalliz'", 'symmetrical': 'False', 'to': "orm['dalliz.Category_sub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_sub_level_2']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_main': {
            'Meta': {'object_name': 'Category_main'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_sub_level_1': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_1'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_main']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.category_sub_level_2': {
            'Meta': {'unique_together': "(('name', 'parent_category'),)", 'object_name': 'Category_sub_level_2'},
            'cookie': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Category_sub_level_1']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999'})
        },
        'ooshop.history': {
            'Meta': {'object_name': 'History'},
            'availability': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewProduct']"}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.ShippingArea']", 'null': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.monoprix_matching': {
            'Meta': {'object_name': 'Monoprix_matching'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matching_monoprix_ooshop'", 'to': "orm['monoprix.Product']"}),
            'ooshop_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Product']"}),
            'score': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.newbrand': {
            'Meta': {'object_name': 'NewBrand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'ooshop.newproduct': {
            'Meta': {'object_name': 'NewProduct'},
            'avertissements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.NewBrand']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooshop.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'composition': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conseils': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'conservation': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'goodie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '9999999999999999999999L'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'informations': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'origine': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'package_measure': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'package_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'package_unit': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'unique': 'True', 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Unit']", 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'ooshop.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Brand']", 'null': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooshop.Category_final']", 'null': 'True', 'symmetrical': 'False'}),
            'dalliz_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_product_dalliz_product'", 'null': 'True', 'to': "orm['dalliz.Product']"}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'monoprix_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ooshop_monoprix_product'", 'null': 'True', 'to': "orm['monoprix.Product']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Unit']", 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'})
        },
        'ooshop.product_history': {
            'Meta': {'object_name': 'Product_history'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.Product']"}),
            'promotion': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'promotion_type': ('django.db.models.fields.CharField', [], {'max_length': '9999'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ooshop_promotion_lot'", 'symmetrical': 'False', 'to': "orm['ooshop.Product']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        'ooshop.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'after': ('django.db.models.fields.FloatField', [], {}),
            'before': ('django.db.models.fields.FloatField', [], {}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ooshop.NewProduct']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '9999', 'null': 'True'}),
            'shipping_area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ooshop.ShippingArea']", 'null': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'s'", 'max_length': '1'})
        },
        'ooshop.shippingarea': {
            'Meta': {'object_name': 'ShippingArea'},
            'city_name': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shipping_area': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postal_code': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'ooshop.unit': {
            'Meta': {'object_name': 'Unit'},
            'dalliz_unit': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'ooshop_unit_dalliz_unit'", 'null': 'True', 'to': "orm['dalliz.Unit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['ooshop']
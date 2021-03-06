#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from django.contrib.auth.models import User

from rest_framework import serializers, pagination
from dalliz.models import Category, Brand

from apps.api.helper import ApiHelper

class DallizBrandField(serializers.RelatedField):
	def to_native(self, value):
		brand_match = value.brandmatch_set.all()
		brand = {}
		if len(brand_match)>0:
			dalliz_brand = brand_match[0].dalliz_brand
			brand = {
				'name': dalliz_brand.name,
				'mdd':dalliz_brand.is_mdd,
				}
		return brand

class CategoryURLField(serializers.CharField):
	def to_native(self, category):
		url = category.url
		if category.parent_category is not None:
			url = category.parent_category.url + '/'+ url
		return url

class CategorySerializer(serializers.ModelSerializer):
	url = CategoryURLField(source = '*')
	class Meta:
		model = Category
		exclude = ('tags',)

	@staticmethod
	def all(category = None, leaves = False, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		"""
			This class method return all category architecture.
		"""
		categories = CategorySerializer.get_subs_dalliz(category)
		serialized = []
		if category is not None and category.parent_category is not None and category.category_set.all().count()>0 and leaves:
			# Adding promotion category here
			serialized.append(CategorySerializer.category_promotion_agregate(category = category, osm_name = osm_name, osm_type=osm_type, osm_location=osm_location))

		for c in categories:
			data = CategorySerializer(c).data
			data.update({
				'subs': CategorySerializer.all(c)
			})
			if len(data['subs'])>0:
				data['leave'] = False
			else:
				data['leave'] = True
				if leaves:
					products = ApiHelper.get_products_query_set(c, type_fetched = 'products', osm_name = osm_name , osm_type=osm_type, osm_location=osm_location)
					products_count = products.count() # Adding total count of products in category

					# Now getting brands information
					brands = set([ p.brand.brandmatch_set.all()[0].dalliz_brand for p in products[:] if p.brand is not None and p.brand.brandmatch_set.all().count()==1])
					brands_count = len(brands)
					# Updating data
					data['count'] = products_count
					data['brands'] = {'count': brands_count, 'content': BrandSerializer(brands, many = True).data}

			serialized.append(data)
		return serialized

	@staticmethod
	def category_promotion_agregate(category = None, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		"""
			Return pomotions summary for a category that is not a leaf but is a direct parent to a leaf category.
		"""
		query_set = ApiHelper.get_products_query_set(category, type_fetched = 'promotions', osm_name = osm_name , osm_type=osm_type, osm_location=osm_location)
		
		promotions = {
			'id': category.id, # Putting parent catgory as id for promotions
			'name': 'promotions',
			'leave': True,
			'parent_category': category.id,
			'position': 0,
			'subs': [],
			'brands': {'count':0, 'content':[]},
			'url': category.url+"/promotions"
		}

		# Removing duplicates
		products = query_set.all()
		promotions['count']= len(products)

		# Now getting brands information
		promotions['brands']['content'] = set([ p.brand.brandmatch_set.all()[0].dalliz_brand for p in list(products) if p.brand is not None and p.brand.brandmatch_set.all().count()==1])
		promotions['brands']['count'] = len(promotions['brands']['content'])

		# Serializing brands
		promotions['brands']['content'] = BrandSerializer(promotions['brands']['content'], many = True).data

		return promotions

	@staticmethod
	def get_subs_dalliz(category = None):
		if category:
			return Category.objects.filter(parent_category = category).order_by('position')
		else:
			return Category.objects.filter(parent_category__isnull = True).order_by('position')



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ('password', 'groups', 'user_permissions')


class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand


# Deafult Pagination Serializer
class NextPageField(serializers.Field):
	"""
	Field that returns a link to the next page in paginated results.
	"""
	page_field = 'page'

	def to_native(self, value):
		if not value.has_next():
	   		return None
		page = value.next_page_number()
		return page

class PreviousPageField(serializers.Field):
	"""
	Field that returns a link to the previous page in paginated results.
	"""
	page_field = 'page'

	def to_native(self, value):
		if not value.has_previous():
			return None
		page = value.previous_page_number()
		return page

class PaginationSerializer(pagination.PaginationSerializer):
	"""
	A default implementation of a pagination serializer.
	"""
	count = serializers.Field(source='paginator.count')
	next = NextPageField(source='*')
	previous = PreviousPageField(source='*')
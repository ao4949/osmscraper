#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

from dalliz.models import Category, Brand

def ApiHelper(objects):
	"""
		This class is created in order to simplify the api view code.
		It only contains static methods.
	"""

	@staticmethod
	def get_subs_dalliz(category = None):
		if category:
			return Category.objects.filter(parent_category = category).order_by('position')
		else:
			return Category.objects.filter(parent_category__isnull = True).order_by('position')

	@staticmethod
	def all(category = None, leaves = False, osm_name = 'monoprix', osm_type='shipping', osm_location=None):
		"""
			This class method return all category architecture.
		"""
		categories = ApiHelper.get_subs_dalliz(category)
		serialized = []
		if category is not None and category.parent_category is not None and category.category_set.all().count()>0 and leaves:
			# Adding promotion category here
			serialized.append(ApiHelper.category_promotion_agregate(category = category, osm_name = osm_name, osm_type=osm_type, osm_location=osm_location))

		for c in categories:
			data = ApiHelper(c).data
			data.update({
				'subs': ApiHelper.all(c)
			})
			if len(data['subs'])>0:
				data['leave'] = False
			else:
				data['leave'] = True
				if leaves:
					# Getting count of products and brands
					# Settings location kwargs :
					kwargs_location_history = {}
					if osm_name == 'monoprix':
						if osm_location is None:
							kwargs_location_history['history__store__isnull'] = True
						else:
							kwargs_location_history['history__store__id'] = osm_location
					else:
						if osm_location is None:
							kwargs_location_history['history__shipping_area__isnull'] = True
						else:
							kwargs_location_history['history__shipping_area__id'] = osm_location

					kwargs = {
						'exists':True,
					}
					kwargs.update(kwargs_location_history) # adding location filter
					products = getattr(c, osm_name+'_product_dalliz_category').filter(**kwargs).distinct('reference')

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
		categories = ApiHelper.get_subs_dalliz(category)
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
		products = []

		# Getting promtions
		for c in categories:
			# Getting count of products and brands
			# Settings location kwargs :
			kwargs_location_promotion = {}
			if osm_name == 'monoprix':
				if osm_location is None:
					kwargs_location_promotion['history__store__isnull'] = True
				else:
					kwargs_location_promotion['history__store__id'] = osm_location
			else:
				if osm_location is None:
					kwargs_location_promotion['history__shipping_area__isnull'] = True
				else:
					kwargs_location_promotion['history__shipping_area__id'] = osm_location

			kwargs = {
				'exists':True,
			}
			kwargs.update(kwargs_location_promotion) # adding location filter
			kwargs.update({'promotion__id__isnull': False, 'promotion__type' : 's'}) # Only handeling simple promotions
			products = products + list(getattr(c, osm_name+'_product_dalliz_category').filter(**kwargs).distinct('reference'))

		# Removing duplicates
		products = set(products)
		promotions['count']= len(products)

		# Now getting brands information
		promotions['brands']['content'] = set([ p.brand.brandmatch_set.all()[0].dalliz_brand for p in list(products) if p.brand is not None and p.brand.brandmatch_set.all().count()==1])
		promotions['brands']['count'] = len(promotions['brands']['content'])

		# Serializing brands
		promotions['brands']['content'] = BrandSerializer(promotions['brands']['content'], many = True).data

		return promotions

	@staticmethod
	def get_products_query_set():
		"""
			Returns query set corresponding to query filters
		"""
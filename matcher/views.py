#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import # Import because of modules names

import pystache
import simplejson as json
import hashlib
from time import time
import re
import itertools

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from ooshop.models import Category as OoshopCategory
from monoprix.models import Category as MonoprixCategory
from auchan.models import Category as AuchanCategory
from dalliz.models import Category as DallizCategory
from ooshop.models import NewProduct as OoshopProduct
from monoprix.models import NewProduct as MonoprixProduct
from auchan.models import Product as AuchanProduct
from matcher.models import ProductSimilarity
from matcher.models import ProductMatch



available_osms = {
	'auchan':{
		'category': AuchanCategory,
		'product': AuchanProduct,
		'query':{
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'ooshop', monoprix_product__id = p['id']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'auchan', query_name = 'monoprix', ooshop_product__id = p['id']).order_by('-score')[:1]],
		}
	},
	'monoprix':{
		'category': MonoprixCategory,
		'product': MonoprixProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'auchan', monoprix_product__id = p['id']).order_by('-score')[:1]],
			'ooshop':lambda p: [serialize_product(sim.ooshop_product, 'ooshop') for sim in ProductSimilarity.objects.filter(index_name = 'monoprix', query_name = 'ooshop', monoprix_product__id = p['id']).order_by('-score')[:1]],

		} 
	},
	'ooshop':{
		'category': OoshopCategory,
		'product': OoshopProduct,
		'query':{
			'auchan':lambda p: [serialize_product(sim.auchan_product, 'auchan') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'auchan', monoprix_product__id = p['id']).order_by('-score')[:1]],
			'monoprix':lambda p: [serialize_product(sim.monoprix_product, 'monoprix') for sim in ProductSimilarity.objects.filter(index_name = 'ooshop', query_name = 'monoprix', ooshop_product__id = p['id']).order_by('-score')[:1]],
		}
	}
}

def serialize_product(product, osm):
	return {
				'id': product.id,
				'osm': osm,
				'url':product.url,
				'image_url':product.image_url,
				'name':product.name,
				'comment': product.comment,
				'brand':(lambda x: x.brand.name if x.brand is not None else '')(product),
				'unit_price':(lambda x: x[0].unit_price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'price': (lambda x: x[0].price if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'quantity': (lambda x: int(x[0].price/x[0].unit_price*1000)/1000.0 if len(x)>0 else 0 )(product.history_set.all().order_by('-created')),
				'unit':(lambda x: x.name if x is not None else 'Unknown')(product.unit),
				'possible_categories': [[{'id':x.id, 'name':x.name} for x in c.dalliz_category.all()] for c in product.categories.all()][0],
				'categories': [{'id':x.id, 'name':(lambda i: i.parent_category.name+' / '+i.name if i.parent_category is not None else i.name)(x)} for x in product.dalliz_category.all()],
				'tags': [{'name':tag.name, 'id':tag.id} for tag in product.tag.all()],
				'possible_tags':list(itertools.chain(*[[[{'id':t.id, 'name':t.name} for t in x.tags.all()] for x in c.dalliz_category.all()] for c in product.categories.all()][0]))
			}

def category(request, osm, category_id):
	# Getting dalliz category
	response = {}
	dalliz_category = DallizCategory.objects.filter(id = category_id)
	if len(dalliz_category) == 0:
		response['status'] = 404
		response['msg'] = 'Dalliz category not found'
	else:
		dalliz_category = dalliz_category[0]

		# Getting osm corresponding categories
		if osm not in available_osms:
			response['status'] = 404
			response['msg'] = 'Osm not available'
		else:
			Category = available_osms[osm]['category']
			osm_categories = Category.objects.filter(dalliz_category = dalliz_category)

			# Get products for each category
			response['categories'] = []
			for cat in osm_categories:
				try:
					products = [ serialize_product(p, osm) for p in cat.newproduct_set.all()  ]
				except Exception, e:
					products = [ serialize_product(p, osm) for p in cat.product_set.all()  ]

				# gettings similarities
				for p in products:
					p['similarities'] = {}
					for osm_index in available_osms:
						if osm != osm_index:
							p['similarities'][osm_index] =  available_osms[osm]['query'][osm_index](p)

				response['categories'].append( {
					'name' : cat.name,
					'id' : cat.id,
					'products' : products
				})
		response['category'] = {
			'name': dalliz_category.name,
			'osm': osm
		}

	# return HttpResponse(json.dumps(response))

	return render(request, 'matcher/category.html', response);

def comment(request, osm, product_id):
	"""
		Saves product comment.
	"""
	response = {}
	if request.method == 'POST':
		comment = request.POST['comment']
		if comment is not None:
			if osm in available_osms:
				Product = available_osms[osm]['product']
				product = Product.objects.filter(id = product_id)
				if len(product)==0:
					response['status'] = 404
					response['msg'] = 'Product Not found, not able to save comment'
				else:
					product = product[0]
					product.comment = comment
					product.save()
					response['status'] = 200
			else:
				response['status'] = 404
				response['msg'] = 'Osm not handled'
	
		else:
			response['status'] = 404
			response['msg'] = 'No comment was sent'
	else:
		response['status'] = 404
		response['msg'] = 'Not handling this method'

	return HttpResponse(json.dumps(response))


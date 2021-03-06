#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import # Import because of modules names

import datetime

from apps.matcher.ooshop.ooshopindexcontroller import OoshopProductIndexController
from apps.matcher.monoprix.monoprixindexcontroller import MonoprixProductIndexController
from apps.matcher.auchan.auchanindexcontroller import AuchanProductIndexController
from apps.matcher.ooshop.ooshopindexcontroller import OoshopBrandIndexController
from apps.matcher.monoprix.monoprixindexcontroller import MonoprixBrandIndexController
from apps.matcher.auchan.auchanindexcontroller import AuchanBrandIndexController
from apps.matcher.dalliz.dallizindexcontroller import DallizBrandIndexController


from apps.matcher.models import MatcherLog
from apps.matcher.models import ProductSimilarity
from apps.matcher.models import BrandSimilarity


class Matcher(object):
	"""
		This class is responsible for managing the different indexes.
		It detects when new documents are added to the database, creates similarities between documents
		and save matches in database.

		TODO : Merge tag list.

	"""
	DEFAULT_INDEXER_CLASSES = []
	def __init__(self, indexer_classes = DEFAULT_INDEXER_CLASSES, LogEntity = MatcherLog, SimilarityEntity = ProductSimilarity):
		self.indexers = [ c() for c in indexer_classes]
		self.products = None
		self.LogEntity = LogEntity
		self.SimilarityEntity = SimilarityEntity

	def set_new_documents(self):
		time_filter = None
		self.documents = {}
		for indexer in self.indexers:
			name = indexer.name
			type = indexer.type
			# Getting time of last matcher process for this osm
			logs = self.LogEntity.objects.filter(name = name, type = type).order_by('-created')
			if len(logs)>0:
				time_filter = logs[0].created

			self.documents[name] = indexer.get_documents(time_filter)

	def set_all_documents(self):
		self.documents = { indexer.name:indexer.get_documents() for indexer in self.indexers}

	def get_indexer_by_name(self, name):
		"""
			Return indexer matching name
		"""
		result_indexer = None
		for indexer in self.indexers:
			if name == indexer.name:
				result_indexer = indexer
				break
		return result_indexer

	def run(self, override = False):
		"""
			This method will go through every indexer, get new products and perform query.
			It will then save the similarities into the database.
		"""

		if not override:
			# Update with new documents
			self.set_new_documents()

			# Update all indexes
			for name, documents in self.documents.iteritems():
				# New documents detected, building new index for corresponding indexer
				indexer = self.get_indexer_by_name(name)
				indexer.add_documents(documents)
		else:
			# Set all documents
			self.set_all_documents()
			# Cleaning all indexes amd rebuilding
			[[indexer.service.drop_index()] for indexer in self.indexers]
			[[indexer.build_all_index()] for indexer in self.indexers]

		
		# Performing queries
		for name_query, documents in self.documents.iteritems():
			for indexer in self.indexers:
				if name_query == indexer.name:
					# Do not perform query
					continue
				print 'Performing %s to %s'%(name_query, indexer.name)
				# Performing query
				similarities = [ {'id':document['id'], 'indexer_name':indexer.name, 'query_name':name_query, 'sims': indexer.query(document)} for document in documents]
				self.save_log(name_query, indexer.type)
				self.clean_database(before = datetime.datetime.now(), index_name = indexer.name, query_name =name_query)
				self.save_similarities(similarities)

	def save_similarities(self, similarities):
		"""
			To be implemented in child class.
		"""
		pass

	def clean_database(self, before, index_name, query_name):
		"""
			Removes database entities that are not in the exclude list.
		"""
		self.SimilarityEntity.objects.filter(index_name = index_name, query_name = query_name, created__lte = before).delete()


	def save_log(self, name, type):
		"""
			Saving log for name
		"""
		self.LogEntity(name = name, type = type).save()

class ProductMatcher(Matcher):
	"""
		This class is responsible for managing the different indexes of osms products.
		It detects when new products are added to the database, creates similarities between products
		and save matches in database.

	"""
	DEFAULT_INDEXER_CLASSES = [OoshopProductIndexController, MonoprixProductIndexController, AuchanProductIndexController]
	def __init__(self, indexer_classes = DEFAULT_INDEXER_CLASSES):
		super(ProductMatcher, self).__init__(indexer_classes, MatcherLog, ProductSimilarity)

	def save_similarities(self, similarities):
		"""
			Saving similarities to database

			Input : 
				- similarities = [{'id':, 'indexer_name':, 'query_name':, 'sims': [(id, score, ??)]}]
		"""
		similarities_db_list = []
		LIMIT_BATCH = 1000
		for s in similarities:
			ooshop_product_id = None
			monoprix_product_id = None
			auchan_product_id = None

			if s['query_name'] == 'ooshop':
				ooshop_product_id = s['id']
			if s['query_name'] == 'monoprix':
				monoprix_product_id = s['id']
			if s['query_name'] == 'auchan':
				auchan_product_id = s['id']

			for id_doc, score, last_arg in s['sims']:
				if s['indexer_name'] == 'ooshop':
					ooshop_product_id = id_doc
				if s['indexer_name'] == 'monoprix':
					monoprix_product_id = id_doc
				if s['indexer_name'] == 'auchan':
					auchan_product_id = id_doc


				if score >.1:
					sim_db = self.SimilarityEntity(
						query_name = s['query_name'],
						index_name = s['indexer_name'],
						monoprix_product_id = monoprix_product_id,
						ooshop_product_id = ooshop_product_id,
						auchan_product_id = auchan_product_id,
						score = score
					)
					similarities_db_list.append(sim_db)
				if len(similarities_db_list)>=LIMIT_BATCH:
					# Creating data in bulk
					self.SimilarityEntity.objects.bulk_create(similarities_db_list, batch_size = LIMIT_BATCH)
					similarities_db_list = []

		# Dealing with left overs
		if len(similarities_db_list) != 0:
			# Creating data in bulk
			self.SimilarityEntity.objects.bulk_create(similarities_db_list, batch_size = LIMIT_BATCH)
			similarities_db_list = []

class BrandMatcher(Matcher):
	"""
		This class is responsible for managing the different indexes of osms brands.
		It detects when new brands are added to the database, creates similarities between brands
		and saves matches in database.

	"""
	DEFAULT_INDEXER_CLASSES = [OoshopBrandIndexController, MonoprixBrandIndexController, AuchanBrandIndexController, DallizBrandIndexController]
	def __init__(self, indexer_classes = DEFAULT_INDEXER_CLASSES):
		super(BrandMatcher, self).__init__(indexer_classes, MatcherLog, BrandSimilarity)

	def set_new_documents(self):
		self.documents = {}
		for indexer in self.indexers:
			name = indexer.name
			type = indexer.type
			self.documents[name] = indexer.get_documents()

	def save_similarities(self, similarities):
		"""
			Saving similarities to database

			Input : 
				- similarities = [{'id':, 'indexer_name':, 'query_name':, 'sims': [(id, score, ??)]}]
		"""
		similarities_db_list = []
		LIMIT_BATCH = 100
		for s in similarities:
			ooshop_brand_id = None
			monoprix_brand_id = None
			auchan_brand_id = None
			dalliz_brand_id = None

			if s['query_name'] == 'ooshop':
				ooshop_brand_id = s['id']
			if s['query_name'] == 'monoprix':
				monoprix_brand_id = s['id']
			if s['query_name'] == 'auchan':
				auchan_brand_id = s['id']
			if s['query_name'] == 'dalliz':
				dalliz_brand_id = s['id']

			for id_doc, score, last_arg in s['sims']:
				if s['indexer_name'] == 'ooshop':
					ooshop_brand_id = id_doc
				if s['indexer_name'] == 'monoprix':
					monoprix_brand_id = id_doc
				if s['indexer_name'] == 'auchan':
					auchan_brand_id = id_doc
				if s['indexer_name'] == 'dalliz':
					dalliz_brand_id = id_doc

				sim_db = self.SimilarityEntity(
					query_name = s['query_name'],
					index_name = s['indexer_name'],
					monoprix_brand_id = monoprix_brand_id,
					ooshop_brand_id = ooshop_brand_id,
					auchan_brand_id = auchan_brand_id,
					dalliz_brand_id = dalliz_brand_id,
					score = score
				)
				similarities_db_list.append(sim_db)
				if len(similarities_db_list)>=LIMIT_BATCH:
					# Creating data in bulk
					self.SimilarityEntity.objects.bulk_create(similarities_db_list, batch_size = LIMIT_BATCH)
					similarities_db_list = []

		# Dealing with left overs
		if len(similarities_db_list) != 0:
			# Creating data in bulk
			self.SimilarityEntity.objects.bulk_create(similarities_db_list, batch_size = LIMIT_BATCH)
			similarities_db_list = []





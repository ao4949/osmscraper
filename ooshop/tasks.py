#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from django.conf import settings
from django.core.mail import send_mail

from celery import Celery
from celery.task import periodic_task, task
from celery.task.schedules import crontab


from scrapers.ooshop.ooshopscraper import OoshopScraper


celery = Celery('tasks', broker=settings.BROKER_URL)

@celery.task
def get_categories():
	"""
		This task is reponsible for retrieving all categories.
	"""
	scraper = OoshopScraper()
	scraper.get_all_categories()

	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()

@celery.task
def get_products_category(categories):
	"""
		This task is reponsible for retrieving products of a category and location.

		Input :
			- categories = [{
				'url':...,
				'location':...
			}]
	"""
	scraper = OoshopScraper()

	for category in categories:
		scraper.get_list_products_for_category(category_url = category['url'], location = category['location'], save = True)
		# time.sleep(1) # Temporisation in order not to flood server


	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()

@celery.task
def get_products(products):
	"""
		This task is reponsible for retrieving products of a product and location.

		Input :
			- products = [{
				'url':...,
				'location':...
			}]
	"""
	scraper = OoshopScraper()

	for product in products:
		try:
			url = product['url']
			location = None
			if 'location' in product:
				location = product['location']
			scraper.get_product_info(product_url = url, location = location, save = True)
			# time.sleep(1) # Temporisation in order not to flood server
		except Exception, e:
			print 'Error in get_products tasks :'
			print product
			print e


	# VERY IMPORTANT, ALWAYS CALL THIS TASK IN ORDER TO HAVE AN INFINITE LOOP
	what_to_do_next.delay()



@celery.task
def what_to_do_next():
	scraper = OoshopScraper()
	rule = scraper.what_to_do_next()

	if rule['type'] == 'categories':
		get_categories.delay()
	elif rule['type'] == 'category_products':
		categories = rule['categories']
		get_products_category.delay(categories = categories)
	elif rule['type'] == 'products':
		products = rule['products']
		get_products.delay(products = products)
	elif rule['type'] == 'global':
		delay = rule['delay']
		what_to_do_next.apply_async(countdown=delay)

# @celery.periodic_task(run_every=crontab(minute="*/60"))
@celery.task
def simple_update():
	from ooshop.models import NewProduct as Product
	from datetime import datetime, timedelta
	scraper = OoshopScraper()
	# First get uncomplete products
	products = Product.objects.filter(exists = True, url__isnull = False, stemmed_text__isnull = True)

	if len(products) >0:
		scraper.get_product_info(products[0].url, save=True)
		simple_update.apply_async(countdown = 2)
	else:
		products = Product.objects.filter(exists = True, url__isnull = False, updated__lte=datetime.now()-timedelta(hours = 24))
		if len(products)>0:
			scraper.get_product_info(products[0].url, save=True)
			simple_update.apply_async(countdown = 2)
		else:
			simple_update.apply_async(countdown = 3600)




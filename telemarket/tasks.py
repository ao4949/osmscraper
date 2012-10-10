#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery.task.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from celery import Celery

from scrapers.telemarket import Telemarket
from models import *

celery = Celery('tasks', broker=settings.BROKER_URL)
telemarket = Telemarket()

def save_categories(categories):
	# Firt we extract main categories from dictonary
	categories_final_objects = []


	for name_category in categories:
		print "Saving category "+name_category+" to database"
		url_category = categories[name_category]["url"]
		category, created = Category_main.objects.get_or_create(name = unicode(name_category), url = unicode(url_category))

		sub_categories = categories[name_category]["sub_categories"]

		for name_category_sub in sub_categories:
			print "Saving sub category "+name_category_sub+" to database"
			sub_category, sub_created = Category_sub_1.objects.get_or_create(name = unicode(name_category_sub), parent_category = category)
			for name_category_sub_lvl_2 in sub_categories[name_category_sub]:
				print "Saving sub category level 2 "+name_category_sub_lvl_2+" to database"
				url_sub_categories_lvl_2 = sub_categories[name_category_sub][name_category_sub_lvl_2]["url"]
				sub_category_lvl_2, sub_created = Category_sub_2.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category)

				if len(sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"]) == 0:
					sub_category_lvl_3, sub_created = Category_sub_3.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category_lvl_2)
					sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_2), url = unicode(url_sub_categories_lvl_2), parent_category = sub_category_lvl_3)
					save_products(url_sub_categories_lvl_2, sub_category_lvl_4)
				else:
					for name_category_sub_lvl_3 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"]:
						print "Saving sub category level 3 "+name_category_sub_lvl_3+" to database"
						url_sub_categories_lvl_3 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["url"]
						sub_category_lvl_3, sub_created = Category_sub_3.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_2)
						
						if len(sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]) == 0:
							sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_3)
							save_products(url_sub_categories_lvl_3, sub_category_lvl_4)
						else:
							for name_category_sub_lvl_4 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]:
								print "Saving sub category level 4 "+name_category_sub_lvl_4+" to database"
								url_sub_categories_lvl_4 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"][name_category_sub_lvl_4]["url"]
								sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_4), url = unicode(url_sub_categories_lvl_4), parent_category = sub_category_lvl_3)
								save_products(url_sub_categories_lvl_4, sub_category_lvl_4)
	return categories_final_objects

def save_products(url_sub_category, category_final):
	products = telemarket.extract_product_list(url_sub_category)

	for product_name in products:
		product = products[product_name]
		title = product["title"]
		url = product["url"]
		price = product["price"]
		unit_str = product["unit"]
		unit_price = product["unit_price"]
		image_url = product["image_url"]
		promotion_bool = product["promotion"]
		type_promotion = product["type_promotion"]

		# Promotion
		promotion, created_promotion = Promotion.objects.get_or_create(type= unicode(type_promotion))

		# Unit
		unit, created_unit = Unit.objects.get_or_create(name = unit_str)

		print "Saving product "+ title+" to database..."
		product_object, created = Product.objects.get_or_create(category = category_final ,title = unicode(title), url= unicode(url), defaults= {"price" : price, "unit_price" : unit_price, "unit" : unit, "image_url" : unicode(image_url), "promotion" : promotion})

		if not created:
			if product_object.title != unicode(title) or product_object.category != category_final or product_object.price != price or product_object.unit_price != unit_price or product_object.unit != unit or product_object.image_url != unicode(image_url) or product_object.promotion != promotion:
				print "Product changed, saving again"
				product_object.title = unicode(title)
				product_object.category = category_final
				product_object.price = price
				product_object.unit_price = unit_price
				product_object.unit = unit
				product_object.image_url = unicode(image_url)
				product_object.promotion = promotion
				product_object.save()
			else:
				print "Product did not change"

@periodic_task(run_every=crontab(minute=0, hour=23))
def get_telemarket_categories():
	telemarket.get_menu()
	categories = telemarket.get_categories()
	save_categories(categories)

# get_telemarket_categories.delay()
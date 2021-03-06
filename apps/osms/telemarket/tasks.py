#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import connection
from django.core.mail import send_mail

from apps.scrapers.telemarket import Telemarket
from models import *

from osmscraper.utility import dictfetchall

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
					new_references = save_products(url_sub_categories_lvl_2, sub_category_lvl_4)
					send_mail_new_products(new_references)
				else:
					for name_category_sub_lvl_3 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"]:
						print "Saving sub category level 3 "+name_category_sub_lvl_3+" to database"
						url_sub_categories_lvl_3 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["url"]
						sub_category_lvl_3, sub_created = Category_sub_3.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_2)
						
						if len(sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]) == 0:
							sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_3), url = unicode(url_sub_categories_lvl_3), parent_category = sub_category_lvl_3)
							new_references = save_products(url_sub_categories_lvl_3, sub_category_lvl_4)
							send_mail_new_products(new_references)
						else:
							for name_category_sub_lvl_4 in sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"]:
								print "Saving sub category level 4 "+name_category_sub_lvl_4+" to database"
								url_sub_categories_lvl_4 = sub_categories[name_category_sub][name_category_sub_lvl_2]["sub_categories"][name_category_sub_lvl_3]["sub_categories"][name_category_sub_lvl_4]["url"]
								sub_category_lvl_4, sub_created = Category_final.objects.get_or_create(name = unicode(name_category_sub_lvl_4), url = unicode(url_sub_categories_lvl_4), parent_category = sub_category_lvl_3)
								new_references = save_products(url_sub_categories_lvl_4, sub_category_lvl_4)
								send_mail_new_products(new_references)
	return categories_final_objects

def save_products(url_sub_category, category_final):
	products = telemarket.extract_product_list(url_sub_category)
	new_products = []

	for product_name in products:
		product = products[product_name]
		title = product["title"]
		url = product["url"]
		reference = product['reference']
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

		product_object, created = Product.objects.get_or_create(reference = unicode(reference), defaults= {"title": unicode(title), "url": unicode(url),"image_url" : unicode(image_url)})
		if created:
			print "Saving new product "+ title+" to database..."
			new_products.append(product_object.reference)
		else:
			print "Updating product "+ title+" to database..."
			
		categories = product_object.category.filter(id = category_final.id)
		if len(categories) == 0:
			product_object.category.add(category_final)
			print "Adding new category "+unicode(category_final)

		# Saving record
		history = Product_history(telemarket_product = product_object, price = price, unit_price=unit_price, unit= unit, promotion=promotion)
		history.save()

	return new_products

def perform_scraping():
	telemarket.get_menu()
	categories = telemarket.get_categories()
	save_categories(categories)

def send_mail_new_products(new_products_reference):
	if len(new_products_reference>0):
		subject = "New products telemarket"
		message = "New products (%d)\n" %(len(new_products_reference))
		for ref in new_products_reference:
			message = message+"\t%s\n" %(ref)
		send_mail(subject, message, 'admin@dalliz.com', ['ahmed@dalliz.com'], fail_silently=False)


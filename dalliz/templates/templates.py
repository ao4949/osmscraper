#!/usr/bin/python
# -*- coding: utf-8 -*-

import pystache
import os

pystache.View.template_path = os.path.abspath(os.path.dirname(__file__))
pystache.View.template_encoding = 'utf-8'

class Product(pystache.View):
	def set_product(self, product):
		self.__product = product
	
	def product(self):
		return self.__product


class Category(pystache.View):
	def set_products(self, products):
		self.__products = products
	
	def products(self):
		return self.__products

	def set_brands(self, brands):
		self.__brands = brands
	
	def brands(self):
		return self.__brands

	def set_categories(self, categories):
		self.__categories = categories
	
	def categories(self):
		return self.__categories

	def set_parent_category(self, parent_category):
		self.__parent_category = parent_category

	def parent_category(self):
		return self.__parent_category


class Cart(pystache.View):
	def set_cart(self, cart):
		self.__cart = cart
	
	def cart(self):
		return self.__cart

	def set_totals(self, totals):
		self.__totals = totals
	
	def totals(self):
		return self.__totals

class Login(pystache.View):
	pass
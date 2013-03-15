from django.db import models

from dalliz.models import Category as Dalliz_category
from tags.models import Tag as GeneralTag

class ShippingArea(models.Model):
	city_name = models.TextField(null=True)
	postal_code = models.TextField(null=True)
	is_shipping_area = models.BooleanField(default=False)

	def __unicode__(self):
		if self.city_name is not None and self.postal_code is not None:
			return "%s (%s)"%(self.city_name, self.postal_code)
		else:
			return "Default Shipping Area"

class Category(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey('self', null = True)
	url = models.CharField(max_length=9999, null=True, unique = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	exists = models.BooleanField(default = True)

	# Dalliz category association
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="auchan_category_dalliz_category")

	class Meta:
		unique_together = ("name", "parent_category")

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=100, unique = True)

	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	parent_brand = models.ForeignKey('self', null = True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return self.name


class Product(models.Model):
	reference = models.CharField(max_length=9999, null=True, unique = True)
	name = models.CharField(max_length=1000, null = True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	url = models.CharField(max_length=9999, null = True)
	brand = models.ForeignKey(Brand, null = True)
	unit = models.ForeignKey(Unit, null = True)
	image_url = models.CharField(max_length=9999, null = True)
	categories = models.ManyToManyField(Category, null = True)
	tags = models.ManyToManyField(Tag, null = True)
	exists = models.BooleanField(default=True)

	# Product detailed description
	valeur_nutritionnelle = models.TextField(null=True)	
	avantages = models.TextField(null=True)
	conservation = models.TextField(null=True)
	pratique = models.TextField(null=True)
	ingredients = models.TextField(null=True)
	complement = models.CharField(max_length=1000, null = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product
	stemmed_text = models.TextField(max_length=9999999999999999999999, null = True) # stemmed text from product html  

	# Content of product
	package_quantity = models.IntegerField(null=True)
	package_measure = models.FloatField(null=True)
	package_unit = models.TextField(null=True)

	# Final tags and dalliz_categories
	dalliz_category = models.ManyToManyField(Dalliz_category, related_name="auchan_product_dalliz_category")
	tag = models.ManyToManyField(GeneralTag, related_name="auchan_product_tag_dalliz_tag")

	# for admins
	comment = models.TextField(default = "")

	def __unicode__(self):
		if self.name is not None:
			return self.name
		else:
			return self.reference

class History(models.Model):
	product = models.ForeignKey(Product)
	created = models.DateTimeField(auto_now_add=True)
	price = models.FloatField()
	unit_price = models.FloatField(null = True)
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

class Promotion(models.Model):
	SIMPLE = 's'
	MULTI = 'm'
	MORE = 'p'
	UNDEF = 'u'
	TYPES = (
		(SIMPLE, 'simple'),
		(MULTI, 'multi'),
		(MORE, 'plus'),
		(UNDEF, 'undef')
	)
	reference = models.CharField(max_length=9999, null=True)
	url = models.CharField(max_length=9999, null = True)
	type = models.CharField(max_length=1, choices=TYPES, default=UNDEF)
	image_url = models.CharField(max_length=9999, null = True)
	content = models.ManyToManyField(Product)
	before = models.FloatField() # Price before any promotion
	after = models.FloatField() # Price during promotion
	unit_price = models.FloatField(null=True)
	start = models.DateField(null = True)
	end = models.DateField(null = True)
	shipping_area = models.ForeignKey(ShippingArea, null = True)
	availability = models.BooleanField(default = True)
	html = models.TextField(max_length=9999999999999999999999, null = True) # html of product 

	class Meta:
		unique_together = ("reference", "shipping_area")

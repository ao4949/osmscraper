from django.db import models

from dalliz.models import Category_sub as Category_dalliz
from dalliz.models import Brand as Brand_dalliz
from dalliz.models import Unit as Unit_dalliz

class Category_main(models.Model):
	name = models.CharField(max_length=100, unique=True)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

class Category_sub_level_1(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_main)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Category_sub_level_2(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_1)
	url = models.CharField(max_length=9999)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Category_final(models.Model):
	name = models.CharField(max_length=100)
	parent_category = models.ForeignKey(Category_sub_level_2)
	url = models.CharField(max_length=9999)
	dalliz_category = models.ManyToManyField(Category_dalliz, related_name="monoprix_category_final_category_dalliz")

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)
	dalliz_brand = models.ForeignKey(Brand_dalliz, null=True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dalliz_unit = models.ManyToManyField(Unit_dalliz, related_name="monoprix_unit_dalliz_unit")

	def __unicode__(self):
		return self.name

class Product(models.Model):
	reference = models.CharField(max_length=9999, null=True)
	title = models.CharField(max_length=1000)
	url = models.CharField(max_length=9999)
	brand = models.ForeignKey(Brand)
	price = models.FloatField()
	unit_price = models.FloatField()
	unit = models.ForeignKey(Unit)
	image_url = models.CharField(max_length=9999)
	promotion = models.CharField(max_length=9999)
	category = models.ForeignKey(Category_final)

	description = models.TextField(null=True)
	ingredients = models.TextField(null=True)
	valeur_nutritionnelle = models.TextField(null=True)
	conservation = models.TextField(null=True)
	conseil = models.TextField(null=True)
	composition = models.TextField(null=True)

	dalliz_url = models.CharField(max_length=9999, null=True)


	class Meta:
		unique_together = ("title", "url", "category")


	def __unicode__(self):
		return self.title

class Cart(models.Model):
	session_key = models.CharField(max_length=1000, unique= True)
	products = models.ManyToManyField(Product, through='Cart_content')

class Cart_content(models.Model):
	cart = models.ForeignKey(Cart)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=0)

	class Meta:
		unique_together = ("cart", "product")

class User(models.Model):
	first_name = models.CharField(max_length=1000, default='')
	last_name = models.CharField(max_length=1000, default='')
	MAN = 'M'
	WOMAN = 'W'
	UNDEF = ''
	SEX = (
		(MAN, 'Homme'),
		(WOMAN, 'Femme'),
		(UNDEF, '')
	)
	sex = models.CharField(max_length=1, choices=SEX, default=UNDEF)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=1000)
	cart = models.ForeignKey(Cart , null = True)
	created = models.DateTimeField(auto_now_add=True)
	token = models.CharField(max_length=1000, null=True)

	def __unicode__(self):
		return self.first_name+' '+self.last_name

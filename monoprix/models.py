from django.db import models

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

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "parent_category")

class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.name

class Unit(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __unicode__(self):
		return self.name

class Product(models.Model):
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


	class Meta:
		unique_together = ("title", "url", "category")


	def __unicode__(self):
		return self.title
from haystack import indexes

from ooshop.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True, template_name = 'search/indexes/osm/product_text.txt')
	brand = indexes.CharField(model_attr='brand__get_dalliz_brand', default = '')
	osm = indexes.CharField(default='ooshop')

	def get_model(self):
		return Product

	def index_queryset(self, using = None):
		"""
			Used when the entire index for model is updated.
		"""
		return self.get_model().objects.filter(exists = True)

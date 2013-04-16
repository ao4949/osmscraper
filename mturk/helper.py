import hashlib

from django.conf import settings

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion

from mturk.models import Task, ResultTask

from matcher.models import ProductSimilarity


class MturkHelper(object):
	"""
		This class handles task creation for amazon mechanical task service.

		Amazon MTruk is used to crowdsource matching products.

		Initialisation :
			- reference : reference of the product
			- osm_from : the origin osm of a product
			- osm_to : the osm to look into
	"""
	if settings.SANDBOX:
		AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
		AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
	else:
		AWS_SECRET_ACCESS_KEY = 'e6/8e5lcCcESPKT/fe6kYkJtf0+7F2w7459WTJ0v'
		AWS_ACCESS_KEY_ID = 'AKIAIP5JQO7FQX6Q7JAQ'

	def __init__(self, reference = None, osm_from = None, osm_to = None, key = None):
		self.reference = reference
		self.osm_from = osm_from
		self.osm_to = osm_to
		self.key = key
		if key is None:
			self.task = None
		else:
			self.task = self.get_task()

	def generate_key(self):
		if self.key is None and self.osm_from is not None and self.osm_to is not None and self.reference is not None:
			key = '%s-%s-%s'%(self.osm_from, self.osm_to, self.reference)
			self.key = hashlib.md5(key).hexdigest()
			return self.key
		else:
			return None

	def save_task(self):
		if self.generate_key() is not None:
			self.task, created = Task.objects.get_or_create(key = self.key, osm_from = self.osm_from, osm_to = self.osm_to, reference = self.reference)
			self.osm_from = self.task.osm_from
			self.osm_to = self.task.osm_to
			self.reference = self.task.reference


	def get_task(self):
		if self.key is not None:
			task = Task.objects.filter(key = self.key)
			if len(task)>0:
				self.task = task[0]
				self.osm_from = self.task.osm_from
				self.osm_to = self.task.osm_to
				self.reference = self.task.reference

	def get_product_similarities(self):
		kwargs = {
			'query_name': self.osm_from,
			'index_name': self.osm_to,
			self.osm_from+'_product__reference':self.reference,
			self.osm_from+'_product__brand__brandmatch__dalliz_brand__is_mdd':False,
			self.osm_to+'_product__productmatch__isnull': True,
		}
		similarities = ProductSimilarity.objects.filter(**kwargs).order_by('-score')[:11]
		return similarities

	def dump(self):
		similarities = self.get_product_similarities()
		data = []
		for sim in similarities:
			data.append({
				'reference': getattr(sim, self.osm_to+'_product').reference,
				'img': getattr(sim, self.osm_to+'_product').image_url,
				})

		return {
			'product_img': getattr(sim, self.osm_from+'_product').image_url,
			'similarities': data,
		}


	def save_result(self, reference_result, hitId, assignment, workerId = None):
		self.get_task()
		result = ResultTask(
			task = self.task,
			workerId = workerId,
			assignementId = assignment,
			hitId = hitId,
			reference = reference_result
			)
		result.save()

	def send_task(self):
		if self.osm_from is not None and self.osm_to is not None and self.reference is not None:
			mtc = MTurkConnection(aws_access_key_id=MturkHelper.AWS_ACCESS_KEY_ID,
									aws_secret_access_key=MturkHelper.AWS_SECRET_ACCESS_KEY,
									host=settings.HOST)

			title = 'Find the corresponding product'
			description = ('Select the most appropriate answer')
			keywords = 'images, selecting, products, matching'
			self.save_task()

			question = ExternalQuestion('http://www.dalliz.com/mturk/key/%s'%(self.key), 600)
			 
			#--------------- CREATE THE HIT -------------------
			 
			a = mtc.create_hit(question=question,
			               max_assignments=10,
			               title=title,
			               description=description,
			               keywords=keywords,
			               duration = 3600*24*7,
			               reward=0.01)


class ProductMtruckHelper(MturkHelper):
	"""
		Initializing MTruk by product.
	"""

	def __init__(self, product, osm_from, osm_to):
		super(ProductMtruckHelper, self).__init__(product.reference, osm_from, osm_to)
		self.product = product

class CategoryMturkHelper(object):
	"""
		Sending tasks to mturk for all products in Category (Dalliz Category)
	"""

	def __init__(self, category, osm_from, osm_to):
		self.category = category
		self.osm_from = osm_from
		self.osm_to = osm_to
		self.set_products()

	def set_products(self):
		self.products = []

		[[self.products.append(p) for p in c.product_set.filter(
									productmatch__isnull = True,
									brand__brandmatch__dalliz_brand__is_mdd = False)]

		for c in getattr(self.category, self.osm_from+'_category_dalliz_category').all()]
	def send_tasks(self):
		"""
			Sending tasks to amazon mturk.
		"""

		for p in self.products:
			print p
			helper = ProductMtruckHelper(p, self.osm_from, self.osm_to)
			helper.send_task()
		

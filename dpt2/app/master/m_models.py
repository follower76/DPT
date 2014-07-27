from django.db import models

class Version(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'versions'

class User(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=64)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now=True)
	admin = models.BooleanField(default=False)
	guest = models.BooleanField(default=False)
	def __unicode__(self):
		return self.full_name()
	class Meta:
		db_table = 'users'
	def full_name(self):
		return self.first_name + " " + self.last_name

class Property(models.Model):
	version = models.ForeignKey(Version,db_index=True)
	name = models.CharField(max_length=64)
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name_plural = 'properties'
		db_table = 'properties'

class Product(models.Model):
	oid = models.IntegerField()
	version = models.ForeignKey(Version,db_index=True)
	name = models.CharField(max_length=256)
	selectable = models.BooleanField()
	def __unicode__(self):
		return self.name
	class Meta:
		db_table = 'products'

class ProductProperty(models.Model):
	product = models.ForeignKey(Product,db_index=True)
	property = models.ForeignKey(Property,db_index=True)
	value = models.FloatField()
	class Meta:
		verbose_name_plural = 'Product Properties'
		db_table = 'product_properties'

class Function(models.Model):
	oid = models.IntegerField()
	version = models.ForeignKey(Version,db_index=True)
	def __unicode__(self):
		return str(self.id)
	class Meta:
		db_table = 'functions'

class FunctionProperty(models.Model):
	function = models.ForeignKey(Function,db_index=True)
	property = models.ForeignKey(Property,db_index=True)
	value = models.FloatField()
	class Meta:
		verbose_name_plural = 'Function Properties'
		db_table = 'function_properties'

class Round(models.Model):
	version = models.ForeignKey(Version,db_index=True)
	user = models.ForeignKey(User,db_index=True)
	date = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'rounds'

class Poll(models.Model):
	round = models.ForeignKey(Round,db_index=True)
	product_a = models.ForeignKey(Product,related_name='+')
	product_b = models.ForeignKey(Product,related_name='+')
	product_c = models.ForeignKey(Product,related_name='+')
	choice = models.ForeignKey(Product,null=True,related_name='+')
	date = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'polls'

class Result(models.Model):
	round = models.ForeignKey(Round,db_index=True)
	function = models.ForeignKey(Function)
	class Meta:
		db_table = 'results'

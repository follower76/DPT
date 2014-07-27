from django.db import models
# from djangotoolbox.Fields import ListField
import ast
import sys


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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    def __unicode__(self):
        return self.full_name()

    class Meta:
        db_table = 'users'

    def full_name(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.fullname


    def get_short_name(self):
        return self.shortname

    @property
    def is_superuser(self):
        return self.is_admin


    @property
    def is_staff(self):
        return self.is_admin


    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, app_label):
        return self.is_admin
    def __unicode__(self):
        return self.full_name()

    class Meta:
        db_table = 'users'

    def full_name(self):
        return self.first_name + " " + self.last_name


class Property(models.Model):
    version = models.ForeignKey(Version, db_index=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'properties'
        db_table = 'properties'


### Added
class Restaurant(models.Model):
    oid = models.IntegerField()
    version = models.ForeignKey(Version, db_index=True)
    name = models.CharField(max_length=256)
    link = models.URLField()
    #logo = models.ImageField(upload_to='/snackpref-data/images')
    #menu = models.URLField()
    #selectable = models.BooleanField()
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'restaurant'


###
class Product(models.Model):
    oid = models.IntegerField()
    version = models.ForeignKey(Version, db_index=True)
    name = models.CharField(max_length=256)
    selectable = models.BooleanField()
    #	image = models.ImageField(upload_to= '/snackpref-data/40 Meals & Restaurant Logos')
    gem = models.BooleanField()
    #	health= models.IntegerField(default = 0) #placeholder Reinier
    stimuliNum = models.IntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'products'


class ProductProperty(models.Model):
    product = models.ForeignKey(Product, db_index=True)
    property = models.ForeignKey(Property, db_index=True)
    value = models.FloatField()

    class Meta:
        verbose_name_plural = 'Product Properties'
        db_table = 'product_properties'


class Function(models.Model):
    oid = models.IntegerField()
    version = models.ForeignKey(Version, db_index=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'functions'


class FunctionProperty(models.Model):
    function = models.ForeignKey(Function, db_index=True)
    property = models.ForeignKey(Property, db_index=True)
    value = models.FloatField()

    class Meta:
        verbose_name_plural = 'Function Properties'
        db_table = 'function_properties'


class Round(models.Model):
    version = models.ForeignKey(Version, db_index=True)
    user = models.ForeignKey(User, db_index=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rounds'


class Poll(models.Model):
    round = models.ForeignKey(Round, db_index=True)
    product_a = models.ForeignKey(Product, related_name='+')
    product_b = models.ForeignKey(Product, related_name='+')
    product_c = models.ForeignKey(Product, related_name='+')
    choice = models.ForeignKey(Product, null=True, related_name='+')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'polls'


class Result(models.Model):
    round = models.ForeignKey(Round, db_index=True)
    function = models.ForeignKey(Function)

    class Meta:
        db_table = 'results'


#class ListField(models.TextField):
#    __metaclass__ = models.SubfieldBase
#    description = "Stores a python list"
#
#    def __init__(self, *args, **kwargs):
#        super(ListField, self).__init__(*args, **kwargs)
#
#    def to_python(self, value):
#        if not value:
#            value = []
#
#        if isinstance(value, list):
#            return value
#
#        return ast.literal_eval(value)
#
#    def get_prep_value(self, value):
#        if value is None:
#            return value
#
#        return unicode(value)
#
#    def value_to_string(self, obj):
#        value = self._get_val_from_obj(obj)
#        return self.get_db_prep_value(value)

## Added for adaptive 
class BigMatrix(models.Model):
    version = models.ForeignKey(Version, db_index=True)
    matrix = models.CommaSeparatedIntegerField(max_length=sys.maxint)  #ListField()
    #matrix_int = eval(matrix)
    class Meta:
        db_table = 'matrices'
	

from django.contrib import admin

from .models import *


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['version', 'name']
    list_filter = ['version']
    list_search = ['name', ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['oid', 'version', 'name', 'selectable', 'gem', 'stimuliNum', 'restaurant']
    list_search = ['name']


class FunctionPropertyAdmin(admin.ModelAdmin):
    list_display = ['function', 'property', 'value']
    list_search = ['value']
    list_filter = ['function']


admin.site.register(Property, PropertyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FunctionProperty, FunctionPropertyAdmin)
admin.site.register(ProductProperty)
admin.site.register(Round)
admin.site.register(Poll)
admin.site.register(Result)
admin.site.register(Version)
admin.site.register(Restaurant)
admin.site.register(GraphData)

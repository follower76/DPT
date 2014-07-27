from django.conf import settings
from models import *
from PIL import Image
from shortcuts import render, redirect
import datetime
import os
import shutil
import subprocess
import tempfile
import xlrd

def main(request):
	if request.method == 'GET':
		return render(request, 'import.html', {})
	if request.method == 'POST':
		if not 'file' in request.FILES:
			return redirect('/import')
		fh, filename = tempfile.mkstemp()
		for chunk in request.FILES['file'].chunks():
			os.write(fh, chunk)
		try:
			workbook = xlrd.open_workbook(filename)
		except:
			return redirect('/import')
		if workbook.sheet_by_index(0).ncols != workbook.sheet_by_index(1).ncols + 2:
			return redirect('/import')
		sheet = workbook.sheet_by_index(0)
		for row in range(1, sheet.nrows):
			if not sheet.cell(row, 2).value:
				return redirect('/import1')
			try:
				x = int(sheet.cell(row, 1).value)
			except:
				return redirect('/import2')
			for col in range(3, sheet.ncols):
				try:
					x = float(sheet.cell(row, col).value)
				except:
					return redirect('/import3')
		sheet = workbook.sheet_by_index(1)
		for row in range(1, sheet.nrows):
			try:
				x = int(sheet.cell(row, 1).value)
			except:
				return redirect('/import4')
			for col in range(1, sheet.ncols):
				try:
					x = float(sheet.cell(row, col).value)
				except:
					return redirect('/import5')
		version = Version()
		version.save()
		destpath = os.path.join(settings.DATA_ROOT, 'images', str(version.id))
		if os.path.isdir(destpath):
			shutil.rmtree(destpath)
		os.mkdir(destpath)
		properties = []
		sheet = workbook.sheet_by_index(0)
		for col in range(3, sheet.ncols):
			property = Property(version=version, name=sheet.cell(0, col).value)
			property.save()
			properties.append(property)
		for row in range(1, sheet.nrows):
			product = Product(version=version, oid=sheet.cell(row, 1).value, name=sheet.cell(row, 2).value)
			if sheet.cell(row, 0).value:
				product.selectable = True
			else:
				product.selectable = False
			product.save()
			for col in range(3, sheet.ncols):
				product_property = ProductProperty(product=product,
						property=properties[col - 3],
						value=sheet.cell(row, col).value)
				product_property.save()
		sheet = workbook.sheet_by_index(1)
		for row in range(1, sheet.nrows):
			function = Function(version=version, oid=sheet.cell(row, 0).value)
			function.save()
			for col in range(1, sheet.ncols):
				function_property = FunctionProperty(function=function,
						property=properties[col - 1],
						value=sheet.cell(row, col).value)
				function_property.save()
		for product in Product.objects.filter(version=version, selectable=True):
			srcpath = os.path.join(settings.DROPBOX_ROOT, 'products')
			for f in os.listdir(srcpath):
				if f.startswith('%s-'%product.oid):
					im = Image.open(os.path.join(srcpath, f))
					im2 = im.copy()
					im2.thumbnail((200, 350), Image.ANTIALIAS)
					im2.save('%s/%s.png'%(destpath, product.oid), 'PNG')
					im2 = im.copy()
					im2.thumbnail((140, 245), Image.ANTIALIAS)
					im2.save('%s/%st.png'%(destpath, product.oid), 'PNG')
			srcpath = os.path.join(settings.DROPBOX_ROOT, 'products-data')
			for f in os.listdir(srcpath):
				if f.startswith('%s-'%product.oid):
					im = Image.open(os.path.join(srcpath, f))
					im2 = im.copy()
					im2.thumbnail((267, 219), Image.ANTIALIAS)
					im2.save('%s/%sd.png'%(destpath, product.oid), 'PNG')
		srcpath = os.path.join(settings.DROPBOX_ROOT, 'results')
		for product in Product.objects.filter(version=version):
			for f in os.listdir(srcpath):
				if f.startswith('%s-'%product.oid):
					im = Image.open(os.path.join(srcpath, f))
					im2 = im.copy()
					im2.thumbnail((100, 100), Image.ANTIALIAS)
					im2.save('%s/%sr.png'%(destpath, product.oid), 'PNG')
	return redirect('/')

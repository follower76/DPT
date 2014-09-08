from django.core.urlresolvers import reverse
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

from django.http import HttpResponse


def main(request):
    if request.method == 'GET':
        return render(request, 'import.html', {})
    if request.method == 'POST':
        rowStart = 8
        if not 'file' in request.FILES:
            return redirect('/import')
        fh, filename = tempfile.mkstemp()
        for chunk in request.FILES['file'].chunks():
            os.write(fh, chunk)
        try:
            workbook = xlrd.open_workbook(filename)
        except:
            return redirect('/import')
        #if workbook.sheet_by_index(0).ncols != workbook.sheet_by_index(1).ncols + 2:
        #return redirect('/import')
        sheet = workbook.sheet_by_index(0) # Was intially index(0)
        for i in range(rowStart, sheet.ncols):#sheet.nrows):
            if sheet.cell(rowStart, i).value == "STOP":
                ncolumns = i
                #return redirect('/')
                break

        for i in range(ncolumns, sheet.ncols):
            if sheet.cell(rowStart, i).value == "STOP2":
                ncolumns_util = i
                break
            #return HttpResponse(sheet.cell(rowStart, ncolumns_util))

    for row in range(rowStart + 1, sheet.nrows):
        try:
            x = int(sheet.cell(row, ncolumns + 1).value)
        except:
            return redirect('/import4')
        for col in range(ncolumns + 1, ncolumns_util): # Was intially sheet.ncols
            try:
                x = float(sheet.cell(row, col).value)
            except:
                return redirect('/import5')
        version = Version()
        version.save()
        #return HttpResponse("Reached 67")
        #For images
        #		destpath = os.path.join(settings.DATA_ROOT, 'images', str(version.id))
        #		if os.path.isdir(destpath):
        #			shutil.rmtree(destpath)
        #		os.mkdir(destpath)
        properties = []
        #sheet = workbook.sheet_by_index(1) # Was index(1)
        for col in range(7, ncolumns):  # Was (3, sheet.ncols)
            property = Property(version=version, name=sheet.cell(rowStart, col).value) ## was (0
            property.save()
            properties.append(property)
        #return HttpResponse(properties[0].name)
        #-----------------------------------------------------------------------------------------------------
        # Restaurant DATA
        sheet = workbook.sheet_by_index(1)
        for row in range(9, sheet.nrows):
            restaurant = Restaurant(version=version, oid=sheet.cell(row, 0).value, name=sheet.cell(row, 1).value,
                                    link=sheet.cell(row, 2).value)#,menu=sheet.cell(row,6))
            restaurant.save()

        sheet = workbook.sheet_by_index(0)
        for row in range(rowStart + 1, sheet.nrows):
            #print >>sys.stderr, 'version is ' + str(version.id) + ' row is ' + str(row) + ' nrows is ' + str(sheet.nrows)
            product = Product(version=version, oid=sheet.cell(row, 1).value, name=sheet.cell(row, 2).value,
                              restaurant=Restaurant.objects.get(oid=sheet.cell(row, 3).value,
                                                                version=version))#get(oid=sheet.cell(row, 3).value))
            if sheet.cell(row, 0).value:
                product.selectable = True
                product.stimuliNum = oid = sheet.cell(row, 0).value
            else:
                product.selectable = False
            if sheet.cell(row, 5).value == 1: #AC
                product.gem = True
            else:
                product.gem = False
            product.save()
            for col in range(7, ncolumns):
                product_property = ProductProperty(product=product,
                                                   property=properties[col - 7],
                                                   value=sheet.cell(row, col).value)
                product_property.save()

            #		sheet = workbook.sheet_by_index(0)
        for row in range(rowStart + 1, sheet.nrows):
            function = Function(version=version, oid=sheet.cell(row, 1).value)
            function.save()
            for col in range(ncolumns + 1, ncolumns_util):
                function_property = FunctionProperty(function=function, property=properties[col - (ncolumns + 1)],
                                                     value=sheet.cell(row, col).value)
                function_property.save()
            #	return redirect('/')

            ### Import Images ### ### IMPORTANT, once stimuli are up!!! ###
            #		for product in Product.objects.filter(version=version, selectable=True):
            #			srcpath = os.path.join(settings.DROPBOX_ROOT)#, 'products')
            #			for f in os.listdir(srcpath):
            #				if f.startswith('%s-'%product.oid):
            #					im = Image.open(os.path.join(srcpath, f))
            #					im2 = im.copy()
            #					im2 = im2.convert('RGB')
            ###					im2.thumbnail((200, 350), Image.ANTIALIAS)
            #					im2.save('%s/%s.png'%(destpath, product.oid), 'PNG')
            ###					im2 = im.copy()
            ###					im2.thumbnail((140, 245), Image.ANTIALIAS)
            ###					im2.save('%s/%st.png'%(destpath, product.oid), 'PNG')
            ###			srcpath = os.path.join(settings.DROPBOX_ROOT, 'products-data')
            ###			for f in os.listdir(srcpath):
            ###				if f.startswith('%s-'%product.oid):
            ###					im = Image.open(os.path.join(srcpath, f))
            ###					im2 = im.copy()
            ###					im2.thumbnail((267, 219), Image.ANTIALIAS)
            ###					im2.save('%s/%sd.png'%(destpath, product.oid), 'PNG')
            ###		srcpath = os.path.join(settings.DROPBOX_ROOT, 'results')
            ###		for product in Product.objects.filter(version=version):
            ###			for f in os.listdir(srcpath):
            ###				if f.startswith('%s-'%product.oid):
            ###					im = Image.open(os.path.join(srcpath, f))
            ###					im2 = im.copy()
            ###					im2.thumbnail((100, 100), Image.ANTIALIAS)
            ###					im2.save('%s/%sr.png'%(destpath, product.oid), 'PNG')
            #############################################

        ### compare pairs Matrix! ###

        index = -1
        num_stimuli = len(Product.objects.filter(version=version, selectable=True))
        num_functions = len(Function.objects.filter(version=version))
        matrix = []
        #		stimuli_col = ncolumns_util + (num_stimuli + 1)
        for i in range(ncolumns_util, sheet.ncols):
            if sheet.cell(rowStart, i).value == "STOP3":
                stimuli_col = i
                break

        for i in range(1, num_stimuli + 1): # Ranges for stimuli
            for j in range(i + 1, num_stimuli + 1):
                index += 1
                matrix.append([])
                for k in range(1, num_functions + 1):
                    matrix[index].append(int(sheet.cell(k + rowStart, stimuli_col + j).value) - int(
                        sheet.cell(k + rowStart,
                                   stimuli_col + i).value)) # Data will be coming from excel file rank(j) - rank(i)
        #matrix_Obj.save()
        f = open('dpt2Matrix.py', 'w+')
        f.write('Big_Matrix=' + str(matrix))
        f.close()

        return redirect(reverse('start'))

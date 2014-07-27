from models import *
from shortcuts import render, redirect
import tempfile
import subprocess
import os
import datetime
import random

def main(request):
	if 'version' in request.session:
		version = request.session['version']
	else:
		try:
			version = Version.objects.order_by('-id')[0]
		except IndexError:
			version = None
	a = [[],[],[],[]]
	if version:
		products = Product.objects.filter(version=version, selectable=True)
		for i in range(products.count() / 4):
			a[0].append(products[4 * i])
			a[1].append(products[4 * i + 1])
			a[2].append(products[4 * i + 2])
			a[3].append(products[4 * i + 3])
	products = a
	return render(request, 'main.html', {'products':products, 'version':version})

def versions(request):
	versions = Version.objects.all()
	return render(request, 'versions.html', {'versions':versions})

def set_version(request, version_id):
	try:
		version = Version.objects.get(id=version_id)
	except Version.DoesNotExist:
		return redirect('/')
	request.session['version']= version
	return redirect('/')

def start(request):
	if 'version' in request.session:
		version = request.session['version']
	else:
		try:
			version = Version.objects.order_by('-id')[0]
		except IndexError:
			return redirect('/')
	if not request.user.id:
		user = User(guest=True, date_joined=datetime.datetime.now(), last_login=datetime.datetime.now())
		user.save()
		request.session["USER_ID"] = user.id
		return redirect('/start')
	rnd = Round(version=version, user=request.user, date=datetime.datetime.now())
	rnd.save()
	products = Product.objects.filter(version=version, selectable=True)
	a, b, c = random.sample(products, 3)
	poll = Poll(round=rnd, product_a=a, product_b=b, product_c=c, date=datetime.datetime.now())
	poll.save()
	return redirect('/preferences')

def preferences(request):
	try:
		rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
	except IndexError:
		return redirect('/')
	polls = Poll.objects.select_related().filter(round=rnd).order_by('-id')
	if not polls:
		return redirect('/start')
	poll = polls[0]
	return render(request, 'preferences.html', {'poll':poll})

def choose(request):
	if 'version' in request.session:
		version = request.session['version']
	else:
		try:
			version = Version.objects.order_by('-id')[0]
		except IndexError:
			return redirect('/')
	rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
	polls = [p for p in Poll.objects.select_related().filter(round=rnd).order_by('-id')]
	if not polls:
		return redirect('/start')
	poll = polls[0]
	poll.choice = Product.objects.get(id=request.POST['id'])
	poll.save()

	polls.reverse()
	choices = []
	ordered_choices = []
	for poll in polls:
		for p in [poll.product_a,poll.product_b,poll.product_c]:
			if not p in choices:
				choices.append(p)
		not_selected = [p for p in [poll.product_a,poll.product_b,poll.product_c] if p != poll.choice]
		ordered_choices.append([poll.choice, not_selected[0]])
		ordered_choices.append([poll.choice, not_selected[1]])

	property_ids = [x.id for x in Property.objects.filter(version=version)]
	function_ids = [f.id for f in Function.objects.filter(version=version)]
	function_properties = FunctionProperty.objects.select_related().filter(function__id__in=function_ids).values_list('function_id', 'property_id', 'value')
	f_properties = {}
	for fid in function_ids:
		f_properties[fid] = {}
	for p in function_properties:
		f_properties[p[0]][p[1]] = p[2]

	product_properties = ProductProperty.objects.select_related().filter(product__in=choices).values_list('product_id', 'property_id', 'value')
	p_coefficients = {}
	for p in choices:
		p_coefficients[p.id] = {}
	for c in product_properties:
		p_coefficients[c[0]][c[1]] = c[2]

	last_bad_functions = []
	bad_functions = []

	for listing in ordered_choices:
		print listing
		if len(ordered_choices) > 2 and listing == ordered_choices[-2]:
			last_bad_functions = [x for x in bad_functions]
		for function_id in function_ids:
			score_listing = []
			for product in listing:
				score = 0
				for property_id in property_ids:
					score += f_properties[function_id][property_id] * p_coefficients[product.id][property_id]
				score_listing.append(score)
			if score_listing[0] < score_listing[1]:
				if not function_id in bad_functions:
					bad_functions.append(function_id)
	finals = []
	if len(function_ids) - len(bad_functions) == 1:
		finals = [f for f in function_ids if f not in bad_functions]
	if len(function_ids) == len(bad_functions):
		finals = [f for f in function_ids if f not in last_bad_functions]
	if finals:
		for final in finals:
			result = Result(round=rnd,function_id=final)
			result.save()
		return redirect('/results')
	used = []
	for poll in polls:
		used.append(poll.product_a)
		used.append(poll.product_b)
		used.append(poll.product_c)
	products = [p for p in Product.objects.filter(version=version, selectable=True) if p not in used]
	a, b, c = random.sample(products, 3)
	poll = Poll(round=rnd, product_a=a, product_b=b, product_c=c, date=datetime.datetime.now())
	poll.save()
	return redirect('/preferences')

def results(request, page=None):
	if 'version' in request.session:
		version = request.session['version']
	else:
		try:
			version = Version.objects.order_by('-id')[0]
		except IndexError:
			return redirect('/')
	rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
	results = Result.objects.filter(round=rnd)

	property_ids = [x.id for x in Property.objects.filter(version=version)]
	function_ids = [r.function_id for r in results]
	function_properties = FunctionProperty.objects.select_related().filter(function__id__in=function_ids).values_list('function_id', 'property_id', 'value')
	properties = {}
	for p in property_ids:
		properties[p] = 0
	for p in function_properties:
		properties[p[1]] += p[2]
	for i in properties.keys():
		properties[i] /= len(function_ids)

	products = Product.objects.filter(version=version)
	product_properties = ProductProperty.objects.select_related().filter(product__in=products).values_list('product_id', 'property_id', 'value')
	p_coefficients = {}
	for p in products:
		p_coefficients[p.id] = {}
	for c in product_properties:
		p_coefficients[c[0]][c[1]] = c[2]

	products = products.values()
	for product in products:
		score = 0
		for property_id in property_ids:
			score += properties[property_id] * p_coefficients[product['id']][property_id]
		product['score'] = score
	products = sorted(products, key=lambda k: k['score'])
	products.reverse()

	pages = []
	for i in range(len(products) / 8):
		pages.append(products[8 * i:8 * i + 8])

	products = products[:8]

	polls = Poll.objects.filter(round=rnd)
	return render(request, 'results.html', {'results':results, 'products':products, 'polls':polls, 'pages':pages})

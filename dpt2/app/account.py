from django.conf import settings
from django.core.validators import email_re
from models import *
from shortcuts import render, redirect
import datetime
import hashlib

def login(request):
	user = User()
	if request.method == 'GET':
		if 'login-user' in request.session:
			user = request.session['login-user']
		return render(request, 'login.html', {'user':user})
	if request.method == "POST":
		try:
			user = User.objects.get(email=request.POST['email'],
					password=hashlib.sha1(request.POST['password']).hexdigest())
		except:
			pass
	if not user.id:
		user.email = request.POST['email']
		user.errors = ['invalid-login']
		request.session['login-user'] = user
		return redirect('/login')
	user.last_login = datetime.datetime.now()
	user.save()
	request.session["USER_ID"] = user.id
	if 'login-user' in request.session:
		del request.session['login-user']
	if 'version' in request.session:
		del request.session['version']
	return redirect('/')

def logout(request):
	if "USER_ID" in request.session:
		del request.session["USER_ID"]
	if 'version' in request.session:
		del request.session['version']
	return redirect('/')

def signup(request):
	if 'signin-user' in request.session:
		user = request.session['signin-user']
	else:
		user = User()
	if request.method == 'GET':
		return render(request, 'signup.html', {'user':user})
	if request.method == 'POST':
		user.errors = []
		user.email = request.POST['email']
		user.first_name = request.POST['first_name']
		user.last_name = request.POST['last_name']
		user.password = request.POST['password']
		user.password2 = request.POST['password2']
		if not user.email:
			user.errors.append('blank-email')
		else:
			if not email_re.match(user.email):
				user.errors.append('invalid-email')
			elif User.objects.filter(email=user.email):
				user.errors.append('email-exists')
		if not user.password:
			user.errors.append('blank-password')
		elif user.password != user.password2:
			user.errors.append('passwords-dont-match')
		if user.errors:
			request.session['signin-user'] = user
			return redirect('/signup')
		if 'signin-user' in request.session:
			del request.session['signin-user']
		user.date_joined = datetime.datetime.now()
		user.last_login = datetime.datetime.now()
		user.password = hashlib.sha1(user.password).hexdigest()
		if user.email in settings.ADMINS:
			user.admin = True
		if request.user.guest:
			user.id = request.user.id
		user.save()
		request.session['USER_ID'] = user.id
		if 'version' in request.session:
			del request.session['version']
		return redirect('/')

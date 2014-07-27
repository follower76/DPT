from django.conf import settings
from django.utils.importlib import import_module
from app.models import *

class SessionMiddleware(object):
	def process_request(self, request):
		engine = import_module(settings.SESSION_ENGINE)
		if 'session_key' in request.GET:
			session_key = request.GET['session_key']
			request.session = engine.SessionStore(session_key)
		try:
			user = User.objects.get(id=request.session["USER_ID"])
		except:
			user = User()
		request.user = user
		request.session_key = request.COOKIES.get('sessionid', None)

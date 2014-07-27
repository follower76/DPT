from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def render(request, template, data, **kwargs):
	return render_to_response(
			template,
			data,
			context_instance=RequestContext(request),
			**kwargs
			)

def redirect(location):
	return HttpResponseRedirect(location)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.cache import cache_control
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Meta_TopChretien

class IndexView(generic.TemplateView):
	template_name = 'index.html'

class BoardView(generic.TemplateView):
	template_name = 'board.html'

class PixelView(generic.TemplateView):

	@cache_control(must_revalidate=True, max_age=60)
	def get(self, request, pixel):
		user_alt = request.GET.get('user_alt')
		profile_picture = request.GET.get('profile_picture')
		print('The user\'s alt is : {} and his image profile URL is : {}'.format(user_alt, profile_picture))
		#les {} servent à être remplacé par ce qui se trouve entre les parenthèses après .format, dans l'ordre.
		entry = Meta_TopChretien.objects.filter(user_alt=user_alt)

		if entry.exists():
			print('The user is already registered in DB')
		else:
			new_user = Meta_TopChretien(user_alt=user_alt, profile_picture=profile_picture)
			new_user.save()
			print('Saving in database... checking user_alt... here it is : ' + str(entry.first()))

		#Rendering of the pixel
		pixel_image = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
		return HttpResponse(pixel_image, content_type='image/gif')

def online_users(request):
	queryset = Meta_TopChretien.objects.all()
	print('def online_users')
	return render(request, 'online-users.html', {'imgs': queryset})


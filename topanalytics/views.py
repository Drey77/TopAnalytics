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
		nickname = request.GET.get('nickname')
		topuser_id = request.GET.get('topuser_id')
		profile_picture = request.GET.get('profile_picture')
		gender = request.GET.get('gender')
		print('The user\'s nickname is : {}, and his topuser_id is : {}, and his profile picture URL is : {}, and his gender is : {}'
			.format(nickname, topuser_id, profile_picture, gender))
		#les {} servent à être remplacé par ce qui se trouve entre les parenthèses après .format, dans l'ordre.
		entry = Meta_TopChretien.objects.filter(nickname=nickname)

		if entry.exists():
			print('The user is already registered in DB')
		else:
			new_user = Meta_TopChretien(nickname=nickname, topuser_id=topuser_id, profile_picture=profile_picture, gender=gender)
			new_user.save()
			print('Saving in database... checking nickname... here it is : ' + str(entry.first()))

		#Rendering of the pixel
		pixel_image = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
		return HttpResponse(pixel_image, content_type='image/gif')

def online_users(request):
	queryset = Meta_TopChretien.objects.all()
	print('def online_users')
	return render(request, 'online-users.html', {'imgs': queryset})


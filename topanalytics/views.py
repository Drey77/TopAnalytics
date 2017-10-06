#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views.decorators.cache import cache_control
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from .models import WebsiteUser
from ipware.ip import get_real_ip, get_ip
import geoip2.database
from topanalytics import utils

class IndexView(generic.TemplateView):
	template_name = 'index.html'

class BoardView(generic.TemplateView):
	template_name = 'board.html'

class PixelView(generic.TemplateView):

	@cache_control(must_revalidate=True, max_age=60)
	def get(self, request, pixel):
		website_user_id = request.GET.get('website_user_id')
		nickname = request.GET.get('nickname')
		profile_picture = request.GET.get('profile_picture')
		gender = request.GET.get('gender')
		test_ip_address = request.GET.get('ip_address')
		user_city = ""

		if test_ip_address is None:
			ip = get_real_ip(request) or get_ip(request)
			if ip is not None:
				print("We have a real ip address for user " + nickname + ", here it is : " + ip )
				user_city = utils.geoip_city(ip)
				print("city of the user : " + str(user_city))

			else:
				print("We don't have an ip address for user")
		else:
			print("The test ip address is : " + test_ip_address)
			user_city = utils.geoip_city(test_ip_address)
			print("Using geoip_city, city of the user " + nickname + ", is :" + user_city)

		print('The user\'s website_user_id is : {}, his nickname is : {}, his profile picture URL is : {}, his gender is : {}, his city is : {}'
			.format(website_user_id, nickname, profile_picture, gender, user_city))
		#les {} servent à être remplacé par ce qui se trouve entre les parenthèses après .format, dans l'ordre.
		entry = WebsiteUser.objects.filter(website_user_id=website_user_id)
		actual_user = entry.first()
		users_in_DB = WebsiteUser.objects.count()

		if entry.exists():
			last_activity = actual_user.last_active
			print('The user is already registered in DB, last activity was on : ' + str(last_activity))
			actual_user.last_active = timezone.now()
			actual_user.save()
			db_city = actual_user.user_city
			if db_city != user_city:
				db_city = user_city
				entry.update(user_city=db_city)
				print('City updated : ' + db_city)
			print('Activity now updated : ' + str(actual_user.last_active))
		else:
			new_user = WebsiteUser(nickname=nickname, website_user_id=website_user_id, profile_picture=profile_picture, gender=gender, first_entry=timezone.now(), website_id="1", user_city=user_city)
			new_user.save()
			print('Saving in database... checked website_user_id, here it is : ' + str(actual_user))

		print("Number of users in DB : " + str(users_in_DB))

		#Rendering of the pixel
		pixel_image = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
		return HttpResponse(pixel_image, content_type='image/gif')

def online_users(request):
	return render(request, 'online-users.html')

def online_users_display(request):
	objects = WebsiteUser.objects.all()
	now = timezone.now()
	under_a_minute = now - timedelta(minutes=1)
	last_users_active = objects.filter(last_active__range=(under_a_minute, now))
	users_online = last_users_active.count()

	print('refresh of online-users-display view, & number of users online : ' + str(users_online))
	return render(request, 'online-users-display.html', {'imgs': last_users_active, 'users_online': users_online})

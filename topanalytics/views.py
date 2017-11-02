#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.utils import timezone
from djgeojson.views import GeoJSONLayerView
from datetime import datetime, timedelta
from .models import WebsiteUser
from accounts import views, forms
from ipware.ip import get_real_ip, get_ip
import geoip2.database
from django.contrib.gis.geos import Point
from topanalytics import utils

class HomePageView(generic.TemplateView):
	template_name = 'index.html'
	def get(self, request):
		return redirect("online-users")


class BoardView(generic.TemplateView):
	template_name = 'board.html'

class UserCityGeoJSONLayer(GeoJSONLayerView):
	def get_queryset(self):
		last_active = utils.LastActiveUsers()
		last_active_users_with_city = last_active.exclude_unknown_city()
		return last_active_users_with_city

class PixelView(generic.TemplateView):

	@cache_control(must_revalidate=True, max_age=60)
	def get(self, request, pixel):
		website_user_id = request.GET.get('website_user_id') or ""
		nickname = request.GET.get('nickname') or "Visiteur"
		profile_picture = request.GET.get('profile_picture') or ""
		gender = request.GET.get('gender') or "Inconnu"
		test_ip_address = request.GET.get('ip_address')
		user_city = "unknown"
		user_country = "unknown"
		user_coords = ""
		user_lon = 0.0
		user_lat = 0.0
		ip = get_real_ip(request) or get_ip(request)
		ip_db = WebsiteUser.objects.filter(ip_address=ip)

		if profile_picture == "" or profile_picture is None:
			print("profile picture is none")
			profile_picture = 'https://s.topchretien.com/static/img/thumb/user2.png'

		if gender == 'male' or gender == 'm':
			print("Gender is Homme")
			gender = 'Homme'
		elif gender =='female' or gender == 'f':
			print("Gender is Femme")
			gender = 'Femme'

		# Let's check if ip_address from user is in database in case a website_user_id is not given to us.
		# if ip == ip_db:
		# 	# If it matches our db, identify him.
		# 	entry = ip_db
		# 	print("Ip_address exist in DB, using it as entry.")
		# else:
		# 	# else, we keep website_user_id as it is or ""
		if test_ip_address != ip and test_ip_address is not None :
			entry = WebsiteUser.objects.filter(ip_address=test_ip_address)
			ip = test_ip_address
			print("test ip address is used for Entry.")
		else :
			print("real address ip is used")
			entry = WebsiteUser.objects.filter(ip_address=ip)

		#TODO : Si website_user_id = "" ET vérifier son ip et l'identifier
		# par rapport à la BDD. (Cela implique d'ajouter au model les adresses IP).
		# ALORS S'il existe donc, entry = cet utilisateur ip.
		# ET Si le website_user_id est donné, on procède comme d'habitude.
		# SINON on enregistre ce nouvel utilisateur
		actual_user = entry.first()
		users_in_DB = WebsiteUser.objects.count()

		#Do we have an ip address in parameters ?
		if test_ip_address is None:
			#If none, get real ip from user.
			if ip is not None:
				print("We have a real ip address for user " + nickname + ", here it is : " + ip )
						# if utils.geoip_city(ip) == 'France':
						# #With our geoip_city util, if we can't get city location from ip, it returns by default "France"
						# 	user_country = utils.geoip_city(ip)
						# 	print("city location not available, default country : " + str(user_country))
						# else:
				#If we have a city location, let's save it to user_city and get user_country and coordinates
				user_city = utils.geoip_city(ip)
				user_country = utils.geoip_country(ip)
				user_lon = utils.geoip_lon(ip)
				user_lat = utils.geoip_lat(ip)

				print("city name of the user : " + str(user_city) + " and his country name is : " + str(user_country))
				#+ " and coordinates are : " + str(user_lon) +", " + str(user_lat)
			else:
				print("We don't have an ip address for user, so let's set it to \'Inconnu\'")
				# ip = "Inconnu"
		else:
		#Ok we have an ip address sent to us through parameters, let's get the infos.
			print("The test ip address is : " + test_ip_address)
			user_city = utils.geoip_city(test_ip_address)
			user_country = utils.geoip_country(test_ip_address)
			user_lon = utils.geoip_lon(test_ip_address)
			user_lat = utils.geoip_lat(test_ip_address)
			print("Using geoip_city, city of the user " + nickname + ", is :" + user_city + ", and his country is :" + user_country
				+ ", and coordinates are : " + str(user_lon) + ", " + str(user_lat))

		print('The user\'s website_user_id is : {}, his nickname is : {}, his profile picture URL is : {}, his gender is : {}, his city is : {}, his country is : {}'
			.format(website_user_id, nickname, profile_picture, gender, user_city, user_country))
		#les {} servent à être remplacé par ce qui se trouve entre les parenthèses après .format, dans l'ordre.


		#Verify if user exists in DB, then update user info
		if entry.exists():
			last_activity = actual_user.last_active
			print('The user is already registered in DB, last activity was on : ' + str(last_activity))
			actual_user.last_active = timezone.now()
			actual_user.save()
			db_city = actual_user.user_city
			db_country = actual_user.user_country
			db_lon = actual_user.geom.get_x()
			db_profile_picture = actual_user.profile_picture

			if db_city != user_city or db_country != user_country or db_lon != user_lon or ip_db != ip or db_profile_picture != profile_picture :
				#If new data is different than database, let's update it with the new coordinates.
				db_city = user_city
				db_country = user_country
				actual_user.geom.set_coords([user_lon, user_lat])
				actual_user.save()
				entry.update(profile_picture=profile_picture, gender=gender, user_city=db_city, user_country=db_country, ip_address=ip)
				print('City updated for user ' + nickname + ' : ' + db_city + ', coordinates and country updated : ' + db_country)

			print('Activity now updated : ' + str(actual_user.last_active))
		elif website_user_id is None and ip is None:
			print('No website_user_id given and ip is unknown to geoip, so we do nothing')
		else:
			#Create new website user.
			user_coords = Point(user_lon, user_lat)
			new_user = WebsiteUser(nickname=nickname, website_user_id=website_user_id, profile_picture=profile_picture, gender=gender, first_entry=timezone.now(), website_id="1", user_city=user_city, user_country=user_country, geom=user_coords, ip_address=ip)
			new_user.save()
			print('Saving in database... checked website_user_id, here it is : ' + website_user_id)

		print("Number of users in DB : " + str(users_in_DB))

		#Rendering of the pixel
		pixel_image = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
		return HttpResponse(pixel_image, content_type='image/gif')

@login_required (login_url='/login/')
def online_users(request):
	return render(request, 'online-users.html')

def online_users_display(request):

	last_active = utils.LastActiveUsers()
	last_active_users = last_active.get_last_active_users()
	users_online = last_active_users.count()

	print('refresh of online-users-display view, & number of users online : ' + str(users_online))
	return render(request, 'online-users-display.html', {'imgs': last_active_users, 'users_online': users_online})

def map(request):

	last_active = utils.LastActiveUsers()
	last_active_users = last_active.get_last_active_users()
	users_online = last_active_users.count()

	return render(request, 'map.html', {'users_online': users_online})

# class UserFormView(View):
# 	form_class = UserForm
# 	template_name = 'registration_form.html'

# 	# display blank form
# 	def get(self, request):
# 		form = self.form_class(None)
# 		return render(request, self.template_name, {'form': form})

# 	# process form data
# 	def post(self, request):
# 		form = self.form_class(request.POST)

# 		if form.is_valid():

# 			#Double check the entered info, not saving yet to DB
# 			user = form.save(commit=False)

# 			# cleaned (normalized) data then saving to DB
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password']
# 			user.set_password(password)
# 			user.save()

# 			# returns User objects if credentials are correct
# 			user = authenticate(username=username, password=password)

# 			if user is not None:

# 				if user.is_active:
# 					login(request, user)
# 					return redirect('home')
# 			else:
# 				return render(request, self.template_name, {'form': form})

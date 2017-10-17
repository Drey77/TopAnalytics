# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import unicodedata

import geoip2.database
from topanalytics import settings
from ipware.ip import get_real_ip, get_ip
from django.utils import timezone
from datetime import datetime, timedelta
from .models import WebsiteUser

############# GEOIP2 #############
if settings.GEOIP2_DATABASE_PATH:
	geoip_reader = geoip2.database.Reader(settings.GEOIP2_DATABASE_PATH)
else:
	geoip_reader = None

class France(object):

	class country(object):
		iso_code = 'FR'
		name = 'France'

def geoip_city(ip=None, request=None):
	if ip is None and request is not None:
		ip = get_real_ip(request) or get_ip(request)
	else:
		try:
			print("actual ip : " + ip)
			return geoip_reader.city(ip).city.name
		except:
			return France.country.name


def geoip_country(ip=None, request=None):
	if ip is None and request is not None:
		ip = get_real_ip(request) or get_ip(request)
	else:
		try:
			return geoip_reader.city(ip).country.name
		except:
			return France.country.name

	# resolved = geoip_city(ip, request)
	# return (resolved.country.name if resolved.country.iso_code
	#         else resolved.registered_country)

def geoip_lon(ip=None, request=None):
	if ip is None and request is not None:
		ip = get_real_ip(request) or get_ip(request)
	else:
		try:
			return geoip_reader.city(ip).location.longitude
		except:
			return 0

def geoip_lat(ip=None, request=None):
	if ip is None and request is not None:
		ip = get_real_ip(request) or get_ip(request)
	else:
		try:
			return geoip_reader.city(ip).location.latitude
		except:
			return 0


class LastActiveUsers(object):

	##### Get last active users from the last minute #####
	def get_last_active_users(self):
		objects = WebsiteUser.objects.all()
		now = timezone.now()
		under_a_minute = now - timedelta(minutes=1)
		last_active_users = objects.filter(last_active__range=(under_a_minute, now))
		return last_active_users

	def exclude_unknown_city(this_object):
		last_active = this_object.get_last_active_users()
		excluded = last_active.exclude(user_city="unknown")
		return excluded
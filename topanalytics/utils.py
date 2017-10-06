# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import unicodedata

import geoip2.database
from topanalytics import settings
from ipware.ip import get_real_ip, get_ip

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
    resolved = geoip_city(ip, request)
    return (resolved.country if resolved.country.iso_code
            else resolved.registered_country)

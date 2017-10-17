# -*- coding: utf-8 -*-
import datetime

#On importe l'utilisation de la table User de Django
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point

class Website(models.Model):
	account_id = models.CharField(max_length=254, blank=True)
	property_id = models.CharField(max_length=254, blank=True)
	view_id = models.IntegerField(default=0, blank=True)
	view_name = models.CharField(max_length=254, blank=True)
	entry_date = models.DateTimeField('Website entry date', default=timezone.now)
	users = models.ManyToManyField(User, blank=True, related_name='users')
	#Ici  ManyToManyField will create a intermediate table between Website and User.
	def __str__(self):
		return self.view_name

class ActionType(models.Model):
	label = models.CharField(max_length=254, blank=True)
	date_added = models.DateTimeField('date added', default=timezone.now)

	def __str__(self):
		return self.label

	def was_added_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.date_added <= now
	was_added_recently.admin_order_field = 'date_added'
	was_added_recently.boolean = True
	was_added_recently.short_description = 'Added recently ?'


class WebsiteUser(models.Model):
	website_user_id = models.CharField(max_length=254, blank=True, unique=True)
	nickname = models.CharField(max_length=25, blank=True)
	profile_picture = models.CharField(max_length=254, blank=True)
	gender = models.CharField(max_length=254, blank=True)
	first_entry = models.DateTimeField('User\'s first entry date', default=timezone.now)
	last_active = models.DateTimeField('User\'s last active', default=timezone.now, blank=True)
	website = models.ForeignKey(Website, related_name='websiteuser', on_delete=models.CASCADE)
	#Relation Many to One with Website
	user_city = models.CharField(max_length=254, blank=True)
	user_country = models.CharField(max_length=254, blank=True)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null = True, blank=True)
	geom = gismodels.PointField(default=Point(x=0, y=0, srid=4326), blank=True, srid=4326)
	objects = gismodels.GeoManager()

	def __str__(self):
		return self.website_user_id

	def is_still_active(self):
		now = timezone.now()
		return now - datetime.timedelta(minutes=1) <= self.last_active <= now
	is_still_active.admin_order_field = 'is_still_active'
	is_still_active.boolean = True
	is_still_active.short_description = 'Is the user still active ?'
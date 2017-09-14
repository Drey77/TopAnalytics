# -*- coding: utf-8 -*-
import datetime

#On importe l'utilisation de la table User de Django
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


class Website(models.Model):
	account_id = models.CharField(max_length=254, blank=True)
	property_id = models.CharField(max_length=254, blank=True)
	view_id = models.IntegerField(default=0, blank=True)
	view_name = models.CharField(max_length=254, blank=True)
	entry_date = models.DateTimeField('Website entry date', default=timezone.now)
	users = models.ManyToManyField(User, blank=True, related_name='websites')
	#Ici  ManyToManyField créera la table intermédiaire entre Website et User.
	def __str__(self):
		return self.view_name


class Tag(models.Model):
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


class Meta_TopChretien(models.Model):
	nickname = models.CharField(max_length=25, blank=True, unique=True)
	topuser_id = models.CharField(max_length=254, blank=True, unique=True)
	profile_picture = models.CharField(max_length=254, blank=True)
	gender = models.CharField(max_length=254, blank=True)

	def __str__(self):
		return self.nickname
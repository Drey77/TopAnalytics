from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from topanalytics.models import WebsiteUser, Website
from ipware.ip import get_real_ip

class Model_WebsiteUserTestCase(TestCase):

	def setUp(self):
		"""Create new object, new user metadata"""

		new_website = Website.objects.create(account_id="1111", property_id="1111", view_name="topchretien.com")
		new_website_user = WebsiteUser.objects.create(website_user_id="1111", nickname="TestCase", profile_picture ="https://s.topchretien.com/media/75/user/77/photo1_compressed.jpg",
		gender="male", first_entry=timezone.now(), website_id=new_website.id)

	def test_WebsiteUser_can_update_last_active(self):
		"""Verify if we can add a last_active date"""
		TestCase = WebsiteUser.objects.get(website_user_id="1111")
		"""Modify the object"""
		TestCase.last_active = datetime(year=2017, month=9, day=19, hour=22, minute=0, second=0, microsecond=0)

class View_Pixel_Tracker(TestCase):
	#Execute aside from Model_WebsiteUserTestCase
	def setUpClient(self):
		self.client = Client()

	def test_pixel_with_param(self):
		"""SetUp"""
		new_website = Website.objects.create(account_id="1111", property_id="1111", view_name="topchretien.com")
		"""Get request"""
		print(new_website.id)
		response = self.client.get('/pixel/top_user.gif?website_user_id=1111&nickname=TestCase&profile_picture=https://s.topchretien.com/media/75/user/77/photo1_compressed.jpg&gender=male&website_id='+ str(new_website.id))

		"""Check that the response is 200 OK"""
		self.assertEqual(response.status_code, 200)


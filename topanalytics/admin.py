from django.contrib import admin

from .models import Website, WebsiteUser
from leaflet.admin import LeafletGeoAdmin

class WebsiteUserAdmin(LeafletGeoAdmin):
	list_display =('website_user_id', 'nickname', 'profile_picture', 'gender', 'first_entry', 'last_active', 'website', 'user_city', 'user_country', 'latitude', 'longitude', 'geom')

admin.site.register(WebsiteUser, WebsiteUserAdmin)
admin.site.register(Website)
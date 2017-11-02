"""TopAnalytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from djgeojson.views import GeoJSONLayerView
from . models import WebsiteUser
from accounts.views import login_view, register_view, logout_view

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register_view, name='register'),
    url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
    url(r'^board$', views.BoardView.as_view(), name='board'),
    url(r'^pixel/(?P<pixel>\w+).gif$', views.PixelView.as_view(), name='pixel'),
    url(r'^online-users$', views.online_users, name='online-users'),
    url(r'^map$', views.map, name='map'),
    url(r'^online-users-display$', views.online_users_display, name='online-users-display'),
    url(r'^data/$', views.UserCityGeoJSONLayer.as_view(model=WebsiteUser, properties=('nickname', 'profile_picture', 'gender', 'user_city', 'user_country')), name='data'),
]

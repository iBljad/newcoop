from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('newcoop_app.urls')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^search/', include('haystack.urls')),
]

from django.urls import path

from . import views

app_name = 'newcoop_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('request/<int:gamer_request_id>', views.request_detail, name='request_detail_name'),
    path('request_post', views.request_post, name='request_post_name'),
]

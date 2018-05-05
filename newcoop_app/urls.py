from django.urls import path

from . import views

app_name = 'newcoop_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('request/<int:pk>', views.RequestDetailsView.as_view(), name='request_detail'),
    path('request_post', views.request_post, name='request_post_name'),
]

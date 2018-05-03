from django.apps import apps
from django.contrib import admin

for model_name, model in apps.get_app_config('newcoop_app').models.items():
    admin.site.register(model)

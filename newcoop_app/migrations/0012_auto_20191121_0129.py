# Generated by Django 2.0.5 on 2019-11-20 22:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('newcoop_app', '0011_auto_20191121_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamerequest',
            name='language',
        )
    ]

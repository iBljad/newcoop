# Generated by Django 2.0.5 on 2019-11-20 22:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(blank=True, verbose_name='release date')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='GameRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='post published')),
                ('mic_present', models.BooleanField(default=False)),
                ('language', models.IntegerField(choices=[(1, 'Russian'), (2, 'English'), (3, 'Other')])),
                ('request_type', models.IntegerField(
                    choices=[(1, 'Co-op teammate'), (2, 'Squad member'), (3, 'Clan member'), (4, 'Competitor')])),
                ('comment', models.TextField(blank=True, max_length=400)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcoop_app.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcoop_app.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['platform_name'],
            },
        ),
        migrations.CreateModel(
            name='RequestComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, max_length=400)),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='post published')),
                ('request',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcoop_app.GameRequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField()),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='post published')),
                ('request',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcoop_app.GameRequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newcoop_app.Platform'),
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='newcoop_app.Platform'),
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='newcoop_app.Genre'),
        ),
        migrations.AlterUniqueTogether(
            name='requestlikes',
            unique_together={('request', 'user')},
        ),
    ]

# Generated by Django 3.2.11 on 2022-04-27 18:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Musicdata',
            fields=[
                ('acousticness', models.FloatField()),
                ('artists', models.TextField()),
                ('danceability', models.FloatField()),
                ('duration_ms', models.FloatField()),
                ('energy', models.FloatField()),
                ('explicit', models.FloatField()),
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('instrumentalness', models.FloatField()),
                ('key', models.FloatField()),
                ('liveness', models.FloatField()),
                ('loudness', models.FloatField()),
                ('mode', models.FloatField()),
                ('name', models.TextField()),
                ('popularity', models.FloatField()),
                ('release_date', models.TextField(null=True)),
                ('speechiness', models.FloatField()),
                ('tempo', models.FloatField()),
                ('valence', models.FloatField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('is_public', models.BooleanField(default=True)),
                ('like_count', models.BigIntegerField(default='0')),
                ('likes', models.ManyToManyField(blank=True, default=None, related_name='like_playlist', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ManyToManyField(related_name='userid', to=settings.AUTH_USER_MODEL)),
                ('songs', models.ManyToManyField(default=None, related_name='song', to='recommender.Musicdata')),
            ],
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-02 20:04

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190401_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_art',
            field=models.ImageField(default='uploads/albumaart/default.png', upload_to=api.models.art_path),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='track',
            name='mp3',
            field=models.FileField(default='uploads/songs/null.mp3', upload_to=api.models.track_path),
        ),
    ]
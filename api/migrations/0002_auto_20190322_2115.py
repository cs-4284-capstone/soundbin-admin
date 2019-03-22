# Generated by Django 2.1.7 on 2019-03-22 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Runtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.IntegerField()),
                ('seconds', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='track',
            name='albumId',
        ),
        migrations.RemoveField(
            model_name='track',
            name='albumTitle',
        ),
        migrations.RemoveField(
            model_name='track',
            name='runtimeMinutes',
        ),
        migrations.RemoveField(
            model_name='track',
            name='runtimeSeconds',
        ),
        migrations.AddField(
            model_name='album',
            name='releaseDate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.ReleaseDate'),
        ),
        migrations.AddField(
            model_name='album',
            name='runtime',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Runtime'),
        ),
        migrations.AddField(
            model_name='track',
            name='album',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Album'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='runtime',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.Runtime'),
            preserve_default=False,
        ),
    ]

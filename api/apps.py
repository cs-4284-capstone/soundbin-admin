from django.apps import AppConfig

from django.db.models.signals import post_save

from .signals import on_addsong


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        post_save.connect(on_addsong, sender='api.Track')
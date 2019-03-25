from django.urls import path

from . import views

urlpatterns = [
    path('tracks/', views.tracks, name='tracks-all'),
    path('tracks/<int:id>', views.track, name='track-single'),

    path('albums/', views.albums, name='albums-all'),
    path('albums/<int:id>', views.album, name='album-single'),

    path('associate/', views.associate, name='associate-user')
]

from django.urls import path

from . import views

urlpatterns = [
    path('tracks/', views.tracks, name='tracks-all'),
    path('tracks/<int:id>', views.track, name='track-single'),

    path('albums/', views.albums, name='albums-all'),
    path('albums/<int:id>', views.album, name='album-single'),

    path('associate/', views.associate, name='associate-user'),

    path('add_transaction/<str:wallet_id>/<str:songs>', views.add_transaction,
         name='add_transaction'),

    path('send_songs/', views.send_songs, name='send_songs')
]

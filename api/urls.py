from django.urls import path

from . import views

urlpatterns = [
    path('tracks/', views.tracks, name='tracks-all'),
    path('tracks/top', views.tracks_top, name='tracks-top'),
    path('tracks/<int:id>', views.track, name='track-single'),

    path('albums/', views.albums, name='albums-all'),
    path('albums/<int:id>', views.album, name='album-single'),

    path('purchases/<int:purchaseid>/send', views.send_songs, name='send_songs'),

    path('customers/new', views.customer_new, name='customer-new'),
    path('customers/<str:email>/purchases', views.customer_email_purchases, name="customer-email-purchases"),
    path('customers/<int:id>/purchases/new', views.customer_purchase_new, name="customer-purchase-new")
]

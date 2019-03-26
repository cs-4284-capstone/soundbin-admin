from django.urls import path

from . import views

urlpatterns = [
    path('tracks/', views.tracks, name='tracks-all'),
    path('tracks/<int:id>', views.track, name='track-single'),

    path('albums/', views.albums, name='albums-all'),
    path('albums/<int:id>', views.album, name='album-single'),

    path('customers/new', views.customer_new, name='customer-new'),
    path('customers/<int:id>/purchases', views.customer_purchases, name="customer-purchases"),
    path('customers/<int:id>/purchases/new', views.customer_purchase_new, name="customer-purchase-new")
]

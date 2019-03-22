from django.conf.urls import url
from django.urls import include
from rest_framework import routers, serializers, viewsets

from api.models import Track


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track
        fields = ('albumId', 'albumTitle', 'id', 'price', 'runtimeSeconds', 'runtimeMinutes', 'title')


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all().order_by('id')
    serializer_class = TrackSerializer

router = routers.DefaultRouter()
router.register(r'tracks', TrackViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url('^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
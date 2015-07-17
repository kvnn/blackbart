from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include('blackbart.apps.api.urls', namespace='api')),
]

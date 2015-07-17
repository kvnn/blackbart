from django.conf.urls import patterns, url

from rest_framework import generics, permissions

from blackbart.apps.miner.serializers import MessageSerializer
from blackbart.apps.miner.models import Message


class BaseAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MessageSerializer


class MessageList(BaseAPIView):
    def get_queryset(self):
        return Message.objects.all().order_by('-date')


class NewMessageList(BaseAPIView):
    def get_queryset(self):
        return Message.objects.filter(subredditcomment__isnull=True, subredditsubmission__isnull=True)


class TopLevelMessageList(BaseAPIView):
    def get_queryset(self):
        return Message.get_top_level_messages()


class NewTopLevelMessageList(BaseAPIView):
    def get_queryset(self):
        return Message.get_new_top_level_messages()



urlpatterns = patterns('',
    url(r'^v1.0/messages/$', MessageList.as_view()),
    url(r'^v1.0/messages/new/$', NewMessageList.as_view()),
    url(r'^v1.0/messages/top-level/$', TopLevelMessageList.as_view()),
    url(r'^v1.0/messages/top-level/new/$', NewTopLevelMessageList.as_view()),
)

from django.urls import path
# from django.views.decorators.csrf import csrf_exempt

from applications.chat import views
from applications.chat.apps import ChatConfig

app_name = ChatConfig.label

urlpatterns = [
    path("chat/", views.ChatView.as_view(), name="chat"),
    # path("start/", csrf_exempt(views.SmartStartView.as_view()), name="smartStart"),
]

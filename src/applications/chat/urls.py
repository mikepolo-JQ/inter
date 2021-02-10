from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.chat import views
from applications.chat.apps import ChatConfig

# from django.views.decorators.csrf import csrf_exempt


app_name = ChatConfig.label

urlpatterns = [
    path("chat/<int:pk>/", views.ChatView.as_view(), name="chat"),
    path("", views.MessengerView.as_view(), name="messenger"),
    path("create/<int:pk>/", views.ChatCreateView.as_view(), name="create"),
    path("delmsg/<int:pk>/", csrf_exempt(views.DeleteSingleMsgView.as_view()), name="delete_msg"),

    # path("chat/<int:pk>/newmsg/", views.NewMsgView.as_view(), name="new-msg"),
    # path("start/", csrf_exempt(views.SmartStartView.as_view()), name="smartStart"),
]

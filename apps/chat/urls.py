from django.urls import path

from apps.chat.views import ChatApiView

urlpatterns = [
    path("", ChatApiView.as_view()),
]

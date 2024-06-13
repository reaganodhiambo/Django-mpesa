from django.urls import path
from .views import StkPushView, CallbackView

urlpatterns = [
    path("stk-push/", StkPushView.as_view()),
    path("callback/", CallbackView.as_view(), name="callback")
]

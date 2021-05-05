
from django.urls import path

from .models import DeviceInfo
from .views import DeviceView,MessageView

urlpatterns = [
    path('device/',DeviceView.as_view()),
    path('message/',MessageView.as_view()),
    # path('detail/<int:pk>/',DeviceDetail.as_view()),
]
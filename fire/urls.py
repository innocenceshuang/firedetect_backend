
from django.urls import path

from .models import DeviceInfo
from .views import DeviceView,MessageView,DeviceDetail,stop_transmit,MessageDetail,MessageAccount

urlpatterns = [
    path('device/',DeviceView.as_view()),
    path('message/',MessageView.as_view()),
    path('device/<int:id>/',DeviceDetail.as_view()),
    path('message/<int:id>/',MessageDetail.as_view()),
    path('stop/',stop_transmit),
    path('messageCount/',MessageAccount)
    # path('detail/<int:pk>/',DeviceDetail.as_view()),
]
# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# import logging

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apscheduler.schedulers.background import BackgroundScheduler# 使用它可以使你的定时任务在后台运行
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
import redis

from .models import DeviceInfo,Message
from .serializers import DeviceInfoSerializer,MessageSerializer
# Create your views here.

class DeviceView(APIView):
    def get(self,request):
        devices = DeviceInfo.objects.all()
        serializer = DeviceInfoSerializer(devices,many=True)
        return Response(serializer.data)


class MessageView(APIView):
    def get(self,request):
        messages = Message.objects.order_by('-id')
        serializer = MessageSerializer(messages,many=True)
        return Response(serializer.data)













# ======================================================================================================
# 定时查询设备状态
communication = redis.Redis(host='39.101.200.0', port=6379, db=0, password='Wrj145325' )

def updateStatus():
    state = communication.get(1).decode('utf-8')
    origin = DeviceInfo.objects.get(device_id=1)
    DeviceInfo.objects.filter(device_id=1).update(status=state)
    if state=='onfire':
        Message.objects.create(text='Area 1 onfire.',device_id=1)
    elif state!=origin.status:
        Message.objects.create(text='Device 1 '+ state, device_id=1)

try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(),"default")
    scheduler.add_job(
        updateStatus,
        trigger=CronTrigger(second="*/30"),
        id="updateStatus",
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()
except Exception as e:
    print(e)

# ========================================================================================================

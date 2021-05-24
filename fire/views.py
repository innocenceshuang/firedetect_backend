# from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse,JsonResponse
import time
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# import logging
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apscheduler.schedulers.background import BackgroundScheduler# 使用它可以使你的定时任务在后台运行
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
import redis

from .models import DeviceInfo,Message
from .serializers import DeviceInfoSerializer,MessageSerializer,DeviceDetailSerializer,MessageDetailSerializer
# Create your views here.

class DeviceView(APIView):
    def get(self,request):
        devices = DeviceInfo.objects.all()
        serializer = DeviceInfoSerializer(devices,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = DeviceInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceDetail(APIView):
    def get_object(self,id):
        try:
            return DeviceInfo.objects.get(device_id=id)
        except DeviceInfo.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        device = self.get_object(id)
        communication.set('TRASMITDEVICE', id)
        communication.set('STOPTRASMIT', 0)
        serializer = DeviceInfoSerializer(device)
        return Response(serializer.data)

    def delete(self,request,id):
        device = self.get_object(id)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,id):
        device = self.get_object(id)
        serializer = DeviceDetailSerializer(device,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class MessageView(APIView):
    def get(self,request):
        messages = Message.objects.order_by('dealed','-id')
        serializer = MessageSerializer(messages,many=True)
        return Response(serializer.data)


class MessageDetail(APIView):
    def get_object(self,id):
        try:
            return Message.objects.get(id=id)
        except Message.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        message = self.get_object(id)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def put(self,request,id):
        message = self.get_object(id)
        serializer = MessageDetailSerializer(message,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# 停止传输
def stop_transmit(request):
    if request.method == 'GET':
        communication.set('STOPTRASMIT',1)
        print('stop')
        return JsonResponse(data=None,safe=False,status=200)


# 信息统计
def MessageAccount(request):
    if request.method == 'GET':
        messagenum = []
        devices = []
        resentmessages = Message.objects.filter(timestamp__gt=datetime.date.today()-datetime.timedelta(days=30))
        temp = DeviceInfo.objects.all().values('device_id')
        for device in temp:
            device = device['device_id']
            warnNum = resentmessages.filter(device_id=device).aggregate(Count('id'))
            warnNum = warnNum['id__count']
            messagenum.append(warnNum)
            devices.append(device)
        return JsonResponse({'devices':devices,'data':messagenum})

# ======================================================================================================
# 定时查询设备状态
communication = redis.Redis(host='39.101.200.0', port=6379, db=0, password='Wrj145325' )

statuses = {}
lastmesses = {}

# 计数，6次调用报警
count = 0

def updateStatus():
    global statuses
    print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()),end=' ')
    print("sync")
    # 当前监控的所有设备
    devices = DeviceInfo.objects.all().values('device_id')
    for device in devices:
        device = device['device_id']
        print("device {id} updated".format(id=device))
        # 同步设备状态
        state = communication.get(device).decode('utf-8')
        if device in statuses.keys():
            statuses[device].append(state)
        else:
            statuses[device] = []
            statuses[device].append(state)

        origin = DeviceInfo.objects.get(device_id=device)
        DeviceInfo.objects.filter(device_id=device).update(status=state)
        # 保活
        communication.set(device,'offline')
    global count
    count = count+1
    if count==6:
        addWarningMessage(devices)
        statuses = {}
        count = 0
        # 调用报警
        # if state=='onfire':
        #     Message.objects.create(text='Area 1 onfire.',device_id=device)
        # elif state!=origin.status:
        #     Message.objects.create(text='Device 1 '+ state, device_id=device)


def addWarningMessage(devices):
    for device in devices:
        device = device['device_id']
        sensitive = DeviceInfo.objects.get(device_id=device).sensitive
        convert=[0,0,0]
        fire = 0
        fireflag = False
        performances=statuses[device]
        for performance in performances:
            if performance=='onfire':
                fire+=1
        if sensitive == 1:
            if fire>=4:
                fireflag=True

        elif sensitive == 2:
            if fire>=3:
                fireflag=True
        else:
            if fire>=2:
                fireflag=True

        if fireflag==True:
            Message.objects.create(text='Area '+device+' onfire.')
            lastmesses[device] = 'onfire'
        elif performances[-1]=='offline':
            if device in lastmesses.keys():
                if lastmesses[device] != 'offline':
                    Message.objects.create(text='Device ' + device + ' offline.')
            lastmesses[device] = 'offline'
        else:
            lastmesses[device] = 'online'


try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(),"default")
    scheduler.add_job(
        updateStatus,
        trigger=CronTrigger(second="*/5"),
        id="updateStatus",
        max_instances=1,
        replace_existing=True
    )
    scheduler.start()
except Exception as e:
    print(e)

# ========================================================================================================

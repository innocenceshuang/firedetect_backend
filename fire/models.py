from django.db import models


# Create your models here.
# 设备
class DeviceInfo(models.Model):
    # location
    device_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=100,default='unknown')
    status = models.CharField(max_length=20,default='offline') # choices=('onfire','online','offline')
    video_addr = models.CharField(max_length=50)
    sensitive = models.IntegerField(default=2)

    def __str__(self):
        return self.device_id

# 报警消息
class Message(models.Model):
    device = models.ForeignKey(DeviceInfo,on_delete=models.CASCADE,default='')
    text = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    dealed = models.BooleanField(default=False)


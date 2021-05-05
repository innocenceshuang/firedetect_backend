from rest_framework import serializers

from .models import DeviceInfo,Message

class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['device_id', 'text', 'timestamp']


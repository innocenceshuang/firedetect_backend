from rest_framework import serializers

from .models import DeviceInfo,Message

class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = '__all__'

class DeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = ['device_id','sensitive']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'device_id', 'text', 'timestamp','dealed']

class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','dealed']


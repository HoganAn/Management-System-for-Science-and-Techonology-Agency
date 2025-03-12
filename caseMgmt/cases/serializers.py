from abc import ABC

from rest_framework import serializers
from .models import Case, Service, CaseDoc, ServDoc
from users.models import User


class CaseSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ['id', 'case_name', 'case_info', 'date_started', 'date_ended', 'state', 'status']
        read_only_fields = ['status']

    def get_status(self, obj):
        if obj.state:
            return '已完成'
        else:
            return '未完成'


class ServiceSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_info', 'date_started', 'date_ended', 'provider_name',
                  'provider_contact_info', 'state', 'status', 'type']
        read_only_fields = ['status']

    def get_status(self, obj):
        if obj.state:
            return '已完成'
        else:
            return '未完成'


class CaseDocSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    case_name = serializers.SerializerMethodField()

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]

    def get_case_name(self, obj):
        return obj.case_belonged.case_name

    class Meta:
        model = CaseDoc
        fields = '__all__'


class ServDocSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    serv_name = serializers.SerializerMethodField()

    def get_filename(self, obj):
        return obj.file.name.split('/')[-1]

    def get_serv_name(self, obj):
        return obj.serv_belonged.service_name

    class Meta:
        model = ServDoc
        fields = '__all__'

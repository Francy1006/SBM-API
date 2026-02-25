from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import SystemConfig, FranchiseConfig, NotificationTemplate, AuditLog, Status
from .serializers import (
    SystemConfigSerializer, FranchiseConfigSerializer,
    NotificationTemplateSerializer, AuditLogSerializer, StatusSerializer
)

# Create your views here.

class SystemConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SystemConfig
    """
    queryset = SystemConfig.objects.select_related('created_by')   # type: ignore
    serializer_class = SystemConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'created_by']
    search_fields = ['key', 'value', 'description']
    ordering_fields = ['key', 'created_at', 'updated_at']
    ordering = ['key']


class FranchiseConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo FranchiseConfig
    """
    queryset = FranchiseConfig.objects.select_related('franchise', 'created_by')   # type: ignore
    serializer_class = FranchiseConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'franchise', 'created_by']
    search_fields = ['key', 'value', 'description']
    ordering_fields = ['key', 'created_at', 'updated_at']
    ordering = ['franchise', 'key']


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo NotificationTemplate
    """
    queryset = NotificationTemplate.objects.select_related('created_by')   # type: ignore
    serializer_class = NotificationTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['template_type', 'is_active', 'created_by']
    search_fields = ['name', 'subject', 'content']
    ordering_fields = ['name', 'template_type', 'created_at']
    ordering = ['name']


class AuditLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo AuditLog
    """
    queryset = AuditLog.objects.select_related('user', 'franchise')   # type: ignore
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user', 'franchise']
    search_fields = ['object_id', 'details', 'ip_address']
    ordering_fields = ['action', 'created_at']
    ordering = ['-created_at']


class StatusByModuleView(APIView):

    def get(self, request, module):
        queryset = Status.objects.filter(
            module=module,
            is_active=True
        ).order_by("id")

        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)
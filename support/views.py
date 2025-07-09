from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SupportTicket, SupportCategory, SupportResponse, SupportAttachment
from .serializers import (
    SupportTicketSerializer, SupportCategorySerializer,
    SupportResponseSerializer, SupportAttachmentSerializer
)

# Create your views here.

class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SupportTicket
    """
    queryset = SupportTicket.objects.select_related(  # type: ignore
        'created_by', 'assigned_to', 'franchise'
    ).prefetch_related('responses', 'attachments')
    serializer_class = SupportTicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'franchise', 'created_by', 'assigned_to']
    search_fields = ['ticket_number', 'title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'status']
    ordering = ['-created_at']


class SupportCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SupportCategory
    """
    queryset = SupportCategory.objects.all()  # type: ignore
    serializer_class = SupportCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class SupportResponseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SupportResponse
    """
    queryset = SupportResponse.objects.select_related('ticket', 'created_by')  # type: ignore
    serializer_class = SupportResponseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ticket', 'is_internal', 'created_by']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class SupportAttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SupportAttachment
    """
    queryset = SupportAttachment.objects.select_related('ticket', 'response', 'created_by')  # type: ignore
    serializer_class = SupportAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ticket', 'response', 'created_by', 'mime_type']
    search_fields = ['file_name']
    ordering_fields = ['created_at', 'file_size']
    ordering = ['-created_at']

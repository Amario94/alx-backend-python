from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
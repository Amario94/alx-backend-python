# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination

# class MessagePagination(PageNumberPagination):
#     page_size = 20


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 10  # or set as needed

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

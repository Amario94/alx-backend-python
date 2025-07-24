# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested.routers import NestedDefaultRouter
# from .views import ConversationViewSet, MessageViewSet

# router = DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')

# # Nested route: /conversations/{conversation_id}/messages/
# nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
# nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/', include(nested_router.urls)),
#     path('api-auth/', include('rest_framework.urls')),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


# nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
# nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),  # Expose at /api/conversations/
    # path('', include(nested_router.urls)),
    path('auth/', include('rest_framework.urls')),  # Optional
]

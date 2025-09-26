from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")


# Nested router for messages under conversations
conversations_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
]

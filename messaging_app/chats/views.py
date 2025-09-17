from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only conversations the user participants in."""
        return self.queryset.filter(participants_id=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new conversation with the requesting user as a participant."""
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)  # add current user
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.add(*users)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return messages in conversations the user participates in."""
        return self.queryset.filter(
            conversation__participants_id=self.request.user
        ).order_by("-sent_at")

    def perform_create(self, serializer):
        """Set the sender to the requesting user."""
        serializer.save(sender=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        url_path="by-conversation/(?P<conversation_id>[^/.]+)",
    )
    def by_conversation(self, request, conversation_id=None):
        """Get messages for a specific conversation."""
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You do not have access to this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )
        messages = self.get_queryset().filter(conversation=conversation)
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from .pagination import MessagePagination

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "participants__email",
        "participants__first_name",
        "participants__last_name",
    ]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not isinstance(participant_ids, list):
            return Response(
                {"detail": "participants must be a list of UUIDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)
        other_users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.add(*other_users)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body"]
    ordering_fields = ["sent_at"]
    pagination_class = MessagePagination

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.request.query_params.get("conversation")
        qs = Message.objects.filter(conversation__participants=user)
        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)
        return qs.order_by("sent_at")

    def create(self, request, *args, **kwargs):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get("conversation")
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = serializer.save(sender=request.user, conversation=conversation)
        out_serializer = MessageSerializer(message)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

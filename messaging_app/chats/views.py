from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only conversations where the current user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation. Payload:
        {
            "participants": ["uuid1", "uuid2", ...]
        }
        """
        participant_ids = request.data.get("participants", [])
        if not isinstance(participant_ids, list):
            return Response(
                {"detail": "participants must be a list of UUIDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user)  # include current user
        other_users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.add(*other_users)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages in a conversation.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter messages by conversation_id query param:
        GET /messages/?conversation=<uuid>
        """
        qs = self.queryset
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            qs = qs.filter(conversation__conversation_id=conversation_id)
        return qs.order_by("sent_at")

    def create(self, request, *args, **kwargs):
        """
        Send a new message. Payload:
        {
            "conversation": "<conversation_uuid>",
            "message_body": "Hello!"
        }
        """
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get("conversation")
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        # check if user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = serializer.save(sender=request.user, conversation=conversation)
        out_serializer = MessageSerializer(message)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

from rest_framwork import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ["message_id", "sender", "content", "is_read", "sent_at"]
        read_only_fields = ["message_id", "sender", "sent_at"]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError(
                "Message body exceeds maximum length of 1000 characters."
            )
        return value

    def get_sender_full_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id", "messages", "created_at"]

    def get_participant_emails(self, obj):
        return [participant.email for participant in obj.participants_id.all()]

    def get_message_count(self, obj):
        return obj.messages.count()

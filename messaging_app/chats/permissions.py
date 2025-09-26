from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Ensure that the user is a participant of the conversation.
        Assumes your Message model has a foreign key to Conversation,
        and Conversation has participants (ManyToMany or similar).
        """
        conversation = getattr(obj, "conversation", None)
        if conversation is None:
            return False

        return request.user in conversation.participants.all()

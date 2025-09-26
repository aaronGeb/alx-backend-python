from typing import Any
from rest_framework import permissions
from rest_framework.request import Request
from .models import Conversation


ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    of the given conversation or objects related to it.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageOwner(permissions.BasePermission):
    """
    Allows access only to the sender or receiver of a message.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user in {
            getattr(obj, "sender", None),
            getattr(obj, "receiver", None),
        }


class IsConversationParticipant(permissions.BasePermission):
    """
    Allows access only to users who are participants, owners,
    or linked users of a conversation-like object.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # Covers common relationship patterns
        for attr in ["participants", "users"]:
            if hasattr(obj, attr):
                rel = getattr(obj, attr)
                return request.user in (rel.all() if hasattr(rel, "all") else rel)

        if hasattr(obj, "user1") and hasattr(obj, "user2"):
            return request.user in {obj.user1, obj.user2}

        if hasattr(obj, "owner"):
            return request.user == obj.owner

        return False

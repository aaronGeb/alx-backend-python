from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
       
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
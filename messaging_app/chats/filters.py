from django_filters import rest_framework as filters
from .models import Message, Conversation


class MessageFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sender = filters.UUIDFilter(field_name="sender__user_id")

    class Meta:
        model = Message
        fields = ["conversation", "sender", "start_date", "end_date"]


class ConversationFilter(filters.FilterSet):
    participant = filters.UUIDFilter(field_name="participants__user_id")

    class Meta:
        model = Conversation
        fields = ["participant"]

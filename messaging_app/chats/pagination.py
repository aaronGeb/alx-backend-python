from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination for messages.
    Default: 20 messages per page
    Allows client to override with ?page_size=... up to 100 max.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

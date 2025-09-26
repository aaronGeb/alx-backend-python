import logging
from datetime import timedelta
from typing import Callable
from django.utils import timezone
from django.http import HttpResponseForbidden

# Configure logging
logging.basicConfig(
    filename="./requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


class RequestLoggingMiddleware:
    """
    Logs each request with user and path.
    """

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.info("User: %s - Path: %s", user, request.path)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Restricts access outside working hours (9 AM to 6 PM).
    """

    START_HOUR = 9
    END_HOUR = 18

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = timezone.now().hour
        if not (self.START_HOUR <= current_hour < self.END_HOUR):
            return HttpResponseForbidden(
                f"Access is allowed only between {self.START_HOUR}:00 and {self.END_HOUR}:00."
            )
        return self.get_response(request)


class RateLimitMiddleware:
    """
    Rate-limits chat message creation per client IP.
    Example: max 5 messages per minute.
    """

    MAX_MESSAGES = 5
    TIME_WINDOW = timedelta(seconds=60)

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.ip_tracking: dict[str, list] = {}

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path.lower():
            ip = self._get_client_ip(request)
            now = timezone.now()
            window_start = now - self.TIME_WINDOW

            timestamps = [t for t in self.ip_tracking.get(ip, []) if t > window_start]

            if len(timestamps) >= self.MAX_MESSAGES:
                return HttpResponseForbidden(
                    "Message limit exceeded. Please wait before sending more messages."
                )

            timestamps.append(now)
            self.ip_tracking[ip] = timestamps

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request) -> str:
        """
        Extracts client IP address, considering proxies.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")


class RolePermissionMiddleware:
    """
    Ensures only users with allowed roles can perform protected actions.
    """

    ALLOWED_ROLES = {"admin", "moderator"}

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in.")

        if getattr(user, "role", None) not in self.ALLOWED_ROLES:
            return HttpResponseForbidden(
                "You do not have permission to perform this action."
            )

        return self.get_response(request)

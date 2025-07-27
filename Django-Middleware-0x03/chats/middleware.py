# core/middleware.py
import logging
from datetime import datetime, time
from django.http import JsonResponse
from collections import defaultdict
from threading import Lock

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')  # log file will be in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
    


from datetime import datetime, time
from django.http import JsonResponse

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Always allow access to Swagger and Admin
        allowed_paths = ["/swagger/", "/admin/", "/redoc/", "/api/schema/"]
        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        current_time = datetime.now().time()
        start_time = time(6, 0)   # ✅ 6:00 AM
        end_time = time(21, 0)    # ✅ 9:00 PM

        if not (start_time <= current_time <= end_time):
            return JsonResponse(
                {"detail": "Access is restricted outside 6 AM to 9 PM."},
                status=403
            )

        return self.get_response(request)




# Here’s how to implement the OffensiveLanguageMiddleware that 
# limits users to 5 chat messages per minute, based on their IP address:
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(list)  # {ip: [timestamp1, timestamp2, ...]}
        self.lock = Lock()
        self.time_window = 60  # seconds
        self.max_messages = 5

    def __call__(self, request):
        # Only monitor POST requests to the chats API
        if request.method == "POST" and request.path.startswith("/api/chats/"):
            ip = self.get_ip_address(request)
            now = time.time()

            with self.lock:
                # Remove timestamps older than 60 seconds
                self.message_logs[ip] = [
                    timestamp for timestamp in self.message_logs[ip]
                    if now - timestamp < self.time_window
                ]

                if len(self.message_logs[ip]) >= self.max_messages:
                    return JsonResponse(
                        {"detail": "Rate limit exceeded: Max 5 messages per minute."},
                        status=429
                    )

                self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_ip_address(self, request):
        # Check common headers for IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

# Here's how you can implement the RolePermissionMiddleware to check if the user has the
#  role of "admin" or "moderator" before allowing access to certain actions:
# chats/middleware.py doesn't contain: ["class RolepermissionMiddleware"]
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip admin panel or static/media files
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            user_role = getattr(user, 'role', None)  # assuming you have a `role` field in your User model
            if user_role in ['admin', 'moderator']:
                return self.get_response(request)
            else:
                return JsonResponse({'detail': 'Access forbidden: insufficient permissions'}, status=403)
        
        return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=403)

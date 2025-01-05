# middleware.py
from django.http import JsonResponse

class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware executed for:", request.path) 
        try:
            response = self.get_response(request)
        except RuntimeError as e:
            if "APPEND_SLASH" in str(e):
                print("APPEND_SLASH issue detected.") 
                return JsonResponse({
                    "error": "URL must include a trailing slash or set APPEND_SLASH=False in settings."
                }, status=400)
            raise
        return response
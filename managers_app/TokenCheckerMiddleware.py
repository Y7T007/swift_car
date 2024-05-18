import jwt
from django.http import JsonResponse
import os


class TokenCheckerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Skip token check for login URL
        if request.path == '/managers/login':
            return self.get_response(request)

        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Token is missing'}, status=401)

        try:
            secret_key = os.getenv('SECRET_KEY')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            request.user_id = payload['manager_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token is invalid'}, status=401)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

import jwt
from django.http import JsonResponse
import os

class TokenCheckerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/managers/login':
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Token is missing'}, status=401)

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return JsonResponse({'error': 'Invalid token type'}, status=401)
        except ValueError:
            return JsonResponse({'error': 'Invalid token format'}, status=401)

        try:
            secret_key = os.getenv('SECRET_KEY')
            print(f"Middleware Secret Key: {secret_key}")  # Debugging
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            request.user_id = payload['manager_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token is invalid'}, status=401)

        response = self.get_response(request)
        return response

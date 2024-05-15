from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        User = get_user_model()
        user = User.objects.create_user(**data)
        return JsonResponse({"message": "User registered successfully"})
def login(request):
    # handle the login request
    return JsonResponse({"message": "Login view"})

def logout(request):
    # handle the logout request
    return JsonResponse({"message": "Logout view"})

def reset_password(request):
    # handle the reset password request
    return JsonResponse({"message": "Reset password view"})

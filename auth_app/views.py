from django.http import JsonResponse

def login(request):
    # handle the login request
    return JsonResponse({"message": "Login view"})

def logout(request):
    # handle the logout request
    return JsonResponse({"message": "Logout view"})

def reset_password(request):
    # handle the reset password request
    return JsonResponse({"message": "Reset password view"})

from django.http import JsonResponse

def dashboard(request):
    # handle the dashboard request
    return JsonResponse({"message": "Dashboard view"})
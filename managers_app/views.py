import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

from .models import Manager

def view_manager(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    manager_dict = model_to_dict(manager)
    return JsonResponse(manager_dict)

@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Manager = get_user_model()
        data['password'] = make_password(data['password'])
        manager = Manager.objects.create(**data)
        return JsonResponse({"message": "Manager added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def view_all_managers(request):
    managers = Manager.objects.all()
    managers_list = [model_to_dict(manager) for manager in managers]
    return JsonResponse(managers_list, safe=False)

def update_manager(request, manager_id):
    if request.method == 'POST':
        updated_data = json.loads(request.body)
        manager = Manager.objects.get(id=manager_id)
        for key, value in updated_data.items():
            setattr(manager, key, value)
        manager.save()
        return JsonResponse({"message": "Manager updated successfully"})

@csrf_exempt
def remove_manager(request, manager_id):
    if request.method == 'DELETE':
        manager = Manager.objects.get(id=manager_id)
        manager.delete()
        return JsonResponse({"message": "Manager removed successfully"})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Manager = get_user_model()
        data['password'] = make_password(data['password'])
        manager = Manager.objects.create(**data)
        return JsonResponse({"message": "Manager registered successfully"})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        manager = authenticate(request, email=data['email'], password=data['password'])
        if manager is not None:
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid email or password"}, status=400)
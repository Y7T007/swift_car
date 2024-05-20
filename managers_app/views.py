import os

import jwt
from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Manager
from bson.decimal128 import Decimal128
import json
from datetime import date
import datetime

import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Manager

from bson.objectid import ObjectId

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal128):
            return str(obj)
        elif isinstance(obj, date):
            return obj.isoformat()  # convert date to "YYYY-MM-DD" string
        elif isinstance(obj, ObjectId):
            return str(obj)  # convert ObjectId to string
        return super(DecimalEncoder, self).default(obj)






@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            manager = Manager.objects.get(email=email)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == manager.password:
                payload = {
                    'manager_id': str(manager._id),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }
                secret_key = os.getenv('SECRET_KEY')
                print(f"Login Secret Key: {secret_key}")  # Debugging
                token = jwt.encode(payload, secret_key, algorithm='HS256')
                return JsonResponse({'token': token,'manager_id': str(manager._id),'manager_name': manager.name})
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except Manager.DoesNotExist:
            return JsonResponse({'error': 'Manager not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data['password'] = hashed_password
        manager = Manager(**data)
        manager.save()
        return JsonResponse({"message": "Manager added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def view_all_managers(request):
    managers = Manager.objects.all()
    managers_list = [model_to_dict(manager) for manager in managers]
    managers_json = json.dumps(managers_list, cls=DecimalEncoder)
    return HttpResponse(managers_json, content_type='application/json')
def remove_manager(request, manager_id):
    try:
        manager = Manager.objects.get(_id=ObjectId(manager_id))
        manager.delete()
        return JsonResponse({"message": "Manager removed successfully"})
    except Manager.DoesNotExist:
        return JsonResponse({"error": "Manager not found"}, status=404)


def view_manager(request, manager_id):
    try:
        manager = Manager.objects.get(_id=ObjectId(manager_id))
        manager_dict = model_to_dict(manager)
        manager_json = json.dumps(manager_dict, cls=DecimalEncoder)
        return HttpResponse(manager_json, content_type='application/json')
    except Manager.DoesNotExist:
        return JsonResponse({"error": "Manager not found"}, status=404)
@csrf_exempt
def update_manager(request, manager_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            manager = Manager.objects.get(_id=ObjectId(manager_id))
            for key, value in data.items():
                setattr(manager, key, value)
            manager.save()
            manager_dict = model_to_dict(manager)
            manager_json = json.dumps(manager_dict, cls=DecimalEncoder)
            return HttpResponse(manager_json, content_type='application/json')
        except Manager.DoesNotExist:
            return JsonResponse({"error": "Manager not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
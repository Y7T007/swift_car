from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Manager
from bson.decimal128 import Decimal128
import json
from datetime import date

@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        manager = Manager(**data)
        manager.save()
        return JsonResponse({"message": "Manager added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal128):
            return str(obj)
        elif isinstance(obj, date):
            return obj.isoformat()  # convert date to "YYYY-MM-DD" string
        return super(DecimalEncoder, self).default(obj)

def view_all_managers(request):
    managers = Manager.objects.all()
    managers_list = [model_to_dict(manager) for manager in managers]
    managers_json = json.dumps(managers_list, cls=DecimalEncoder)
    return HttpResponse(managers_json, content_type='application/json')
def remove_manager(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
        manager.delete()
        return JsonResponse({"message": "Manager removed successfully"})
    except Manager.DoesNotExist:
        return JsonResponse({"error": "Manager not found"}, status=404)

def view_manager(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
        manager_dict = model_to_dict(manager)
        return JsonResponse(manager_dict)
    except Manager.DoesNotExist:
        return JsonResponse({"error": "Manager not found"}, status=404)

@csrf_exempt
def update_manager(request, manager_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            manager = Manager.objects.get(id=manager_id)
            for key, value in data.items():
                setattr(manager, key, value)
            manager.save()
            return JsonResponse({"message": "Manager updated successfully"})
        except Manager.DoesNotExist:
            return JsonResponse({"error": "Manager not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Client
from bson.decimal128 import Decimal128
import json
from datetime import date

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
def add_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client = Client(**data)
        client.save()
        return JsonResponse({"message": "Client added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def view_all_clients(request):
    clients = Client.objects.all()
    clients_list = [model_to_dict(client) for client in clients]
    clients_json = json.dumps(clients_list, cls=DecimalEncoder)
    return HttpResponse(clients_json, content_type='application/json')

def view_client(request, client_id):
    try:
        client = Client.objects.get(_id=ObjectId(client_id))
        client_dict = model_to_dict(client)
        client_json = json.dumps(client_dict, cls=DecimalEncoder)
        return HttpResponse(client_json, content_type='application/json')
    except Client.DoesNotExist:
        return JsonResponse({"error": "Client not found"}, status=404)

@csrf_exempt
def update_client(request, client_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            client = Client.objects.get(_id=ObjectId(client_id))
            for key, value in data.items():
                setattr(client, key, value)
            client.save()
            client_dict = model_to_dict(client)
            client_json = json.dumps(client_dict, cls=DecimalEncoder)
            return HttpResponse(client_json, content_type='application/json')
        except Client.DoesNotExist:
            return JsonResponse({"error": "Client not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_client(request, client_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(_id=ObjectId(client_id))
            client.delete()
            return JsonResponse({"message": "Client removed successfully"})
        except Client.DoesNotExist:
            return JsonResponse({"error": "Client not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
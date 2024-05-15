from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Agence
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
def add_agency(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        agency = Agence(**data)
        agency.save()
        return JsonResponse({"message": "Agency added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def view_all_agencys(request):
    agencies = Agence.objects.all()
    agencies_list = [model_to_dict(agency) for agency in agencies]
    agencies_json = json.dumps(agencies_list, cls=DecimalEncoder)
    return HttpResponse(agencies_json, content_type='application/json')

def view_agency(request, agency_id):
    try:
        agency = Agence.objects.get(_id=ObjectId(agency_id))
        agency_dict = model_to_dict(agency)
        agency_json = json.dumps(agency_dict, cls=DecimalEncoder)
        return HttpResponse(agency_json, content_type='application/json')
    except Agence.DoesNotExist:
        return JsonResponse({"error": "Agency not found"}, status=404)

@csrf_exempt
def update_agency(request, agency_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            agency = Agence.objects.get(_id=ObjectId(agency_id))
            for key, value in data.items():
                setattr(agency, key, value)
            agency.save()
            agency_dict = model_to_dict(agency)
            agency_json = json.dumps(agency_dict, cls=DecimalEncoder)
            return HttpResponse(agency_json, content_type='application/json')
        except Agence.DoesNotExist:
            return JsonResponse({"error": "Agency not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_agency(request, agency_id):
    if request.method == 'POST':
        try:
            agency = Agence.objects.get(_id=ObjectId(agency_id))
            agency.delete()
            return JsonResponse({"message": "Agency removed successfully"})
        except Agence.DoesNotExist:
            return JsonResponse({"error": "Agency not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
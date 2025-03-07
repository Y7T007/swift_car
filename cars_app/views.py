from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voiture
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
def add_car(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        car = Voiture(**data)
        car.save()
        return JsonResponse({"message": "Car added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def view_all_cars(request):
    cars = Voiture.objects.all()
    cars_list = [model_to_dict(car) for car in cars]
    cars_json = json.dumps(cars_list, cls=DecimalEncoder)
    return HttpResponse(cars_json, content_type='application/json')

def view_car(request, car_id):
    try:
        car = Voiture.objects.get(_id=ObjectId(car_id))
        car_dict = model_to_dict(car)
        car_json = json.dumps(car_dict, cls=DecimalEncoder)
        return HttpResponse(car_json, content_type='application/json')
    except Voiture.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)

@csrf_exempt
def update_car(request, car_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            car = Voiture.objects.get(_id=ObjectId(car_id))
            for key, value in data.items():
                setattr(car, key, value)
            car.save()
            car_dict = model_to_dict(car)
            car_json = json.dumps(car_dict, cls=DecimalEncoder)
            return HttpResponse(car_json, content_type='application/json')
        except Voiture.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_car(request, car_id):
    if request.method == 'POST':
        try:
            car = Voiture.objects.get(_id=ObjectId(car_id))
            car.delete()
            return JsonResponse({"message": "Car removed successfully"})
        except Voiture.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


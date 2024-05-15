from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Voiture
import json

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
    return JsonResponse(cars_list, safe=False)

def remove_car(request, car_id):
    # handle the remove car request
    return JsonResponse({"message": "Remove car view"})



def view_car(request, car_id):
    # handle the view car request
    return JsonResponse({"message": "Hello world : View car view"+str(car_id)})

def update_car(request, car_id):
    # handle the update car request
    return JsonResponse({"message": "Update car view"})
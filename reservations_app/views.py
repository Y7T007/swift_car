from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation
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
def new_reservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reservation = Reservation(**data)
        reservation.save()
        return JsonResponse({"message": "Reservation added successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def view_all_reservations(request):
    reservations = Reservation.objects.all()
    reservations_list = [model_to_dict(reservation) for reservation in reservations]
    reservations_json = json.dumps(reservations_list, cls=DecimalEncoder)
    return HttpResponse(reservations_json, content_type='application/json')

def view_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(_id=ObjectId(reservation_id))
        reservation_dict = model_to_dict(reservation)
        reservation_json = json.dumps(reservation_dict, cls=DecimalEncoder)
        return HttpResponse(reservation_json, content_type='application/json')
    except Reservation.DoesNotExist:
        return JsonResponse({"error": "Reservation not found"}, status=404)

@csrf_exempt
def update_reservation(request, reservation_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            reservation = Reservation.objects.get(_id=ObjectId(reservation_id))
            for key, value in data.items():
                setattr(reservation, key, value)
            reservation.save()
            reservation_dict = model_to_dict(reservation)
            reservation_json = json.dumps(reservation_dict, cls=DecimalEncoder)
            return HttpResponse(reservation_json, content_type='application/json')
        except Reservation.DoesNotExist:
            return JsonResponse({"error": "Reservation not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_reservation(request, reservation_id):
    if request.method == 'POST':
        try:
            reservation = Reservation.objects.get(_id=ObjectId(reservation_id))
            reservation.delete()
            return JsonResponse({"message": "Reservation removed successfully"})
        except Reservation.DoesNotExist:
            return JsonResponse({"error": "Reservation not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
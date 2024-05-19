from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation
from bson.decimal128 import Decimal128
import json
from datetime import date
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.db.models.functions import ExtractWeek
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.db.models.functions import TruncMonth


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


from collections import defaultdict
from datetime import datetime


def sum_prices_per_month(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Initialize a dictionary to store the total price for each month
    prices_per_month = defaultdict(float)

    # Iterate over all reservations
    for reservation in reservations:
        # Extract the month from the date_reservation field
        month = reservation.date_reservation.month

        # Convert the price of the current reservation to a string and then to a float
        price = float(str(reservation.prix))

        # Add the price to the total price for this month
        prices_per_month[month] += price

    # Convert the prices_per_month dictionary to a list of total prices
    result = [prices_per_month[month] for month in sorted(prices_per_month.keys())]

    return JsonResponse(result, safe=False)




def sum_prices_by_week(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Initialize a dictionary to store the total price for each week
    prices_per_week = defaultdict(float)

    # Iterate over all reservations
    for reservation in reservations:
        # Extract the week number from the date_reservation field
        week = reservation.date_reservation.isocalendar()[1]

        # Convert the price of the current reservation to a string and then to a float
        price = float(str(reservation.prix))

        # Add the price to the total price for this week
        prices_per_week[week] += price

    # Convert the prices_per_week dictionary to a list of total prices
    result = [prices_per_week[week] for week in sorted(prices_per_week.keys())]

    return JsonResponse(result, safe=False)

def reservations_per_day(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Initialize a dictionary to store the count of reservations for each day
    reservations_per_day = defaultdict(int)

    # Iterate over all reservations
    for reservation in reservations:
        # Extract the day from the date_reservation field
        day = reservation.date_reservation.toordinal()

        # Increment the count of reservations for this day
        reservations_per_day[day] += 1

    # Convert the reservations_per_day dictionary to a list of counts
    result = [reservations_per_day[day] for day in sorted(reservations_per_day.keys())]

    return JsonResponse(result, safe=False)

def reservations_by_manager(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Initialize a dictionary to store the count of reservations for each manager
    reservations_by_manager = defaultdict(int)

    # Iterate over all reservations
    for reservation in reservations:
        # Extract the manager_id from the reservation
        manager_id = reservation.manager_id

        # Increment the count of reservations for this manager
        reservations_by_manager[manager_id] += 1

    # Sort the reservations_by_manager dictionary by count in descending order and take the top 10
    sorted_reservations_by_manager = sorted(reservations_by_manager.items(), key=lambda item: item[1], reverse=True)[:10]

    # Convert the sorted_reservations_by_manager list to a list of counts
    result = [item[1] for item in sorted_reservations_by_manager]

    return JsonResponse(result, safe=False)

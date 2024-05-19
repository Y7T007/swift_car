from bson import ObjectId
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from managers_app.models import Manager
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


from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

def sum_prices_by_week(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Determine the date 4 weeks ago from the current date
    four_weeks_ago = datetime.now().date() - relativedelta(weeks=4)

    # Filter the reservations to only include those from the last 4 weeks
    reservations = reservations.filter(date_reservation__gte=four_weeks_ago)

    # Initialize a dictionary to store the total price for each of the last 4 weeks
    prices_per_week = {week: 0.0 for week in range(4)}

    # Iterate over all reservations
    for reservation in reservations:
        # Calculate the number of weeks between the reservation date and the current date
        weeks_ago = (datetime.now().date() - reservation.date_reservation).days // 7

        # Convert the price of the current reservation to a string and then to a float
        price = float(str(reservation.prix))

        # Add the price to the total price for the corresponding week
        prices_per_week[weeks_ago] += price

    # Convert the prices_per_week dictionary to a list of total prices
    result = [prices_per_week[week] for week in range(4)]

    return JsonResponse(result, safe=False)

from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

def reservations_per_day(request):
    # Fetch all reservations
    reservations = Reservation.objects.all()

    # Determine the date 4 weeks ago from the current date
    four_weeks_ago = datetime.now().date() - relativedelta(weeks=4)

    # Filter the reservations to only include those from the last 4 weeks
    reservations = reservations.filter(date_reservation__gte=four_weeks_ago)

    # Initialize a dictionary to store the count of reservations for each of the last 28 days
    reservations_per_day = {day: 0 for day in range(28)}

    # Iterate over all reservations
    for reservation in reservations:
        # Calculate the number of days between the reservation date and the current date
        days_ago = (datetime.now().date() - reservation.date_reservation).days

        # Increment the count of reservations for this day
        reservations_per_day[days_ago] += 1

    # Convert the reservations_per_day dictionary to a list of counts
    result = [reservations_per_day[day] for day in range(28)]

    return JsonResponse(result, safe=False)

from django.core.serializers.json import DjangoJSONEncoder
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from django.db.models import Count

class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, Decimal128):
            return str(o)
        return super().default(o)

def reservations_by_manager(request):
    # Fetch all managers and annotate them with the count of their reservations
    managers = Manager.objects.annotate(reservation_count=Count('reservation__manager'))

    # Select the fields to include in the output
    managers = managers.values('_id', 'name', 'date_of_birth', 'gender', 'contact_number', 'address', 'agence_id', 'salary', 'cin', 'email', 'password', 'reservation_count')

    # Convert the QuerySet to a list
    managers_list = list(managers)

    # Convert the list to JSON using the custom encoder
    managers_json = json.dumps(managers_list, cls=JSONEncoder)

    return HttpResponse(managers_json, content_type='application/json')
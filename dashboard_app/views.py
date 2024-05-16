from django.http import JsonResponse
from clients_app.models import Client
from reservations_app.models import Reservation
from cars_app.models import Voiture
from managers_app.models import Manager
from agencies_app.models import Agence
from django.forms import model_to_dict

import json
from bson import ObjectId, Decimal128
from datetime import date

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Decimal128):
            return str(o)
        return json.JSONEncoder.default(self, o)


def dashboard(request):
    # Get all objects from each model
    clients = Client.objects.all()
    reservations = Reservation.objects.all()
    cars = Voiture.objects.all()
    managers = Manager.objects.all()
    agencies = Agence.objects.all()

    # Convert each queryset to a list of dictionaries
    clients_list = [model_to_dict(client) for client in clients]
    reservations_list = [model_to_dict(reservation) for reservation in reservations]
    cars_list = [model_to_dict(car) for car in cars]
    managers_list = [model_to_dict(manager) for manager in managers]
    agencies_list = [model_to_dict(agency) for agency in agencies]

    # Create a dictionary with all the data
    data = {
        'clients': clients_list,
        'reservations': reservations_list,
        'cars': cars_list,
        'managers': managers_list,
        'agencies': agencies_list,
    }

    # Return the data as a JSON response
    return JsonResponse(data, encoder=JSONEncoder)

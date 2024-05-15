import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from .models import Client

def view_client(request, client_id):
    # Fetch the client from the database
    client = Client.objects.get(client_id=client_id)
    # Convert the client object to a dictionary
    client_dict = model_to_dict(client)
    # Return the client data as JSON
    return JsonResponse(client_dict)

@csrf_exempt
def add_client(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        client_data = json.loads(request.body)
        # Create a new client object
        client = Client(**client_data)
        # Save the client object to the database
        client.save()
        # Return a success message
        return JsonResponse({"message": "Client added successfully"})

def view_all_clients(request):
    # Fetch all clients from the database
    clients = Client.objects.all()
    # Convert the clients queryset to a list of dictionaries
    clients_list = [model_to_dict(client) for client in clients]
    # Return the clients data as JSON
    return JsonResponse(clients_list, safe=False)

def update_client(request, client_id):
    # Assume the updated client data is sent in the request body as JSON
    updated_data = request.json()
    # Fetch the client from the database
    client = Client.objects.get(client_id=client_id)
    # Update the client object with the new data
    for key, value in updated_data.items():
        setattr(client, key, value)
    # Save the updated client object to the database
    client.save()
    # Return a success message
    return JsonResponse({"message": "Client updated successfully"})

def remove_client(request, client_id):
    # Fetch the client from the database
    client = Client.objects.get(client_id=client_id)
    # Delete the client
    client.delete()
    # Return a success message
    return JsonResponse({"message": "Client removed successfully"})
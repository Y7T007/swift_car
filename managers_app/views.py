import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from .models import Manager

def view_manager(request, manager_id):
    # Fetch the manager from the database
    manager = Manager.objects.get(manager_id=manager_id)
    # Convert the manager object to a dictionary
    manager_dict = model_to_dict(manager)
    # Return the manager data as JSON
    return JsonResponse(manager_dict)

@csrf_exempt
def add_manager(request):
    try:
        if request.method == 'POST':
            # Parse the JSON data from the request body
            manager_data = json.loads(request.body)
            # Create a new manager object
            manager = Manager(**manager_data)
            manager_data.pop('id', None)

            # Save the manager object to the database
            manager.save()
            # Return a success message
            return JsonResponse({"message": "Manager added successfully"})
    except NotImplementedError:
        return JsonResponse({"error": "An error occurred while adding the manager" }, status=500)

@csrf_exempt
def view_all_managers(request):
    # Fetch all managers from the database
    managers = Manager.objects.all()
    # Convert the managers queryset to a list of dictionaries
    managers_list = [model_to_dict(manager) for manager in managers]
    # Return the managers data as JSON
    return JsonResponse(managers_list, safe=False)

def update_manager(request, manager_id):
    if request.method == 'POST':
        # Parse the updated manager data from the request body
        updated_data = json.loads(request.body)
        # Fetch the manager from the database
        manager = Manager.objects.get(manager_id=manager_id)
        # Update the manager object with the new data
        for key, value in updated_data.items():
            setattr(manager, key, value)
        # Save the updated manager object to the database
        manager.save()
        # Return a success message
        return JsonResponse({"message": "Manager updated successfully"})

@csrf_exempt
def remove_manager(request, manager_id):
    if request.method == 'DELETE':
        # Fetch the manager from the database
        manager = Manager.objects.get(manager_id=manager_id)
        # Delete the manager
        manager.delete()
        # Return a success message
        return JsonResponse({"message": "Manager removed successfully"})
from django.http import JsonResponse

def add_car(request):
    # handle the add car request
    return JsonResponse({"message": "Add car view "+str(request)})

def remove_car(request, car_id):
    # handle the remove car request
    return JsonResponse({"message": "Remove car view"})

def view_all_cars(request):
    # handle the view all cars request
    return JsonResponse({"message": "View all cars view"})

def view_car(request, car_id):
    # handle the view car request
    return JsonResponse({"message": "Hello world : View car view"+str(car_id)})

def update_car(request, car_id):
    # handle the update car request
    return JsonResponse({"message": "Update car view"})
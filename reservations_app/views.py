from django.http import JsonResponse

def new_reservation(request):
    # handle the new reservation request
    return JsonResponse({"message": "New reservation view"})

def view_all_reservations(request):
    # handle the view all reservations request
    return JsonResponse({"message": "View all reservations view"})

def view_reservation(request, reservation_id):
    # handle the view reservation request
    return JsonResponse({"message": "View reservation view"})
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.utils import retrieve_user


def get_user(request, id):
    """
    Retrieve user with a given id
    """
    payload1 = {
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 404
    }
    if request.method != 'GET':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    if not request.user:  # return if user not attached to request from middleware
        return JsonResponse(payload1, status=400)
    try:
        user = retrieve_user(request.user, id)
        if user:
            payload = {
                "status": "success",
                "message": "Successful",
                "data": user,
            }
            return JsonResponse(payload, status=200)
        else:
            return JsonResponse(payload1, status=400)
    except Exception as exc:
        print(f'error getting user from request: {exc}')
        return JsonResponse(payload1, status=400)

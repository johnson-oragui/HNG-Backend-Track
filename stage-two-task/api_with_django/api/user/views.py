import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from user.utils import retrieve_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="Get a user with provided id",
    responses={200: openapi.Response('Success', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT)
        }
    ))}
)


@csrf_exempt
@api_view(['GET'])
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

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.utils import (validate_data, create_user,
                                  generate_token, check_user)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
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
@api_view(['POST'])
def register_user(request):
    """
    API endpoint to Register a user
    """
    payload = {
        "status": "Bad request",
        "message": "Registration unsuccessful",
        "statusCode": 400
    }
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            data, data_valid = validate_data(data)
            if not data_valid:
                return JsonResponse(data, status=422)
            else:
                new_user = create_user(data)
                if new_user:
                    token = generate_token(new_user)
                    payload = {
                        "status": "success",
                        "message": "Registration successful",
                        "data": {
                            "accessToken": token,
                            "user": new_user,
                        }
                    }
                    return JsonResponse(payload, status=200)
                else:
                    return JsonResponse(payload, status=400)
        else:
            return JsonResponse({"error": "method not allowed"}, status=405)
    except Exception as exc:
        print(f'could not register user: {exc}')
        return JsonResponse(payload, status=400)

@swagger_auto_schema(
    method='post',
    operation_description="Authenticates a user",
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
@api_view(['POST'])
def login_user(request):
    """
    Authenticates a user
    """
    payload1 = {
        "status": "Bad request",
        "message": "Authentication failed",
        "statusCode": 401
    }
    try:
        if request.method == 'POST':
            data_body: dict = json.loads(request.body.decode())
            data, is_valid = validate_data(data_body, login=True)
            if not is_valid:
                return JsonResponse(payload1, status=401)
            else:
                user = check_user(data)
                if user:
                    token = generate_token(user)
                    if not token:
                        return JsonResponse(payload1, status=401)
                    payload = {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "accessToken": token,
                            "user": user
                        }
                    }
                    return JsonResponse(payload, status=200)
                else:
                    return JsonResponse(payload1, status=401)
        else:
            return JsonResponse({"error": "Method not allowed!"}, status=405)
    except Exception as exc:
        print(f'error logging in user: {exc}')
        return JsonResponse(payload1, status=401)

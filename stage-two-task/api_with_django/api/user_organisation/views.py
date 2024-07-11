import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_organisation.utils import (get_organzations,
                                     get_organzation,
                                     validate_data,
                                     add_organzation,
                                     add_user_to_organisation)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Retrieves all organisations and Adds a new organisation",
    responses={200: openapi.Response('Success', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': {
                "organisations": openapi.Schema(type=openapi.TYPE_OBJECT)
            }
        }
    ))}
)

@csrf_exempt
@api_view(['GET', 'POST'])
def get_organisations(request):
    """
    Retrieves all organisations

    Adds a new organisation
    """
    payload1 = {
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 400
    }
    if not request.user:
        return JsonResponse(payload1, status=400)
    try:
        if request.method == 'GET':
            all_orgs = get_organzations(request.user)
            payload = {
                "status": "success",
                "message": "Successful",
                "data": {
                    "organisations": all_orgs
                }
            }
            return JsonResponse(payload, status=200)

        elif request.method == 'POST':
            data = json.loads(request.body.decode())
            if not data:
                return JsonResponse(payload1, status=400)
            data = validate_data(data)
            if not data:
                return JsonResponse(payload1, status=400)
            org = add_organzation(data, request.user)
            payload2 = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": org
            }
            return JsonResponse(payload2, status=201)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
    except Exception as exc:
        print(f'error retrieving all organizations: {exc}')
        return JsonResponse(payload1, status=400)

@swagger_auto_schema(
    method='get',
    operation_description="Retrieves a signle organzations with provided id",
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
def get_organisation(request, orgId):
    """
    Retrieves a signle organzations
    """
    payload1 = {
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 400
    }
    try:
        if request.method != 'GET':
            return JsonResponse({"error": "Method not allowed"}, status=405)
        if not request.user:
            return JsonResponse(payload1, status=400)
        org: dict = get_organzation(request.user, orgId)
        payload = {
            "status": "success",
            "message": "Successful",
            "data": org

        }
        return JsonResponse(payload, status=200)
    except Exception as exc:
        print(f'error retrieving a single organizations: {exc}')
        return JsonResponse(payload1, status=400)

@swagger_auto_schema(
    method='post',
    operation_description="Adds a user to an organisation",
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
def add_user(request, orgId):
    """
    Adds a user to an organisation
    """
    payload1 = {
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 400
    }
    if request.method == 'POST':
        if not request.user:
            return JsonResponse(payload1, status=400)
        try:
            data = json.loads(request.body.decode())
            data2 = validate_data(data, user_id=True)
            if data2:
                user_added = add_user_to_organisation(orgId, data, request.user)
                if user_added:
                    payload = {
                        "status": "success",
                        "message": "User added to organisation successfully"
                    }
                    return JsonResponse(payload, status=200)
                else:
                    return JsonResponse(payload1, status=400)
            else:
                return JsonResponse(payload1, status=400)
        except Exception as exc:
            print(f'error adding user to organisation: {exc}')
            return JsonResponse(payload1, status=400)
    else:
        return JsonResponse({"error": "Method not Allowed"}, status=405)

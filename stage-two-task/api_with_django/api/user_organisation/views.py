from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user_organisation.utils import get_organzations, get_organzation


@csrf_exempt
def get_organisations(request):
    """
    Retrieves all organisations
    """
    payload1 = {
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 400
    }
    try:
        if request.method != 'GET':
            return JsonResponse(payload1, status=405)
        if not request.user:
            return JsonResponse(payload1, status=400)
        all_orgs = get_organzations(request.user)
        payload = {
            "status": "success",
            "message": "Successful",
            "data": {
                "organisations": all_orgs
            }
        }
        return JsonResponse(payload, status=200)


    except Exception as exc:
        print(f'error retrieving all organizations: {exc}')
        return JsonResponse(payload1, status=405)

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
            return JsonResponse(payload1, status=405)
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

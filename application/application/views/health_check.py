from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """ヘルスチェック"""
    return JsonResponse(data={"msg": "pass"}, status=status.HTTP_200_OK)

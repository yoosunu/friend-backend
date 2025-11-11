from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core.management import call_command
from django.conf import settings

from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([IsAdminUser])
def migrate_view(request):
    try:
        call_command("makemigrations")
        call_command("migrate", "--noinput")
        return JsonResponse({"status": "ok", "message": "Migration done"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

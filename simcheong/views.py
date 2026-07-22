import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ServerConfig


@csrf_exempt
def config(request):
    if request.method == "GET":
        server_config = ServerConfig.objects.first()

        return JsonResponse({
            "socket": (
                server_config.websocket_url
                if server_config is not None
                else ""
            )
        })

    if request.method == "POST":
        try:
            body = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON body"},
                status=400,
            )

        socket = body.get("socket")

        if not isinstance(socket, str) or not socket.strip():
            return JsonResponse(
                {"error": "socket is required"},
                status=400,
            )

        server_config = ServerConfig.objects.first()

        if server_config is None:
            server_config = ServerConfig.objects.create(
                websocket_url=socket.strip()
            )
        else:
            server_config.websocket_url = socket.strip()
            server_config.save(
                update_fields=["websocket_url", "updated_at"]
            )

        return JsonResponse({
            "socket": server_config.websocket_url
        })

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError


# Create your views here.
class Categories(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(
                categories,
                many=True,
            )
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise NotFound

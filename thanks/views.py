from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from .models import ThanksDate
from .serializers import ThanksDateSerializer, ThanksSerializer


# Create your views here.
class TDs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tds = ThanksDate.objects.filter(user=request.user)
        serializer = ThanksDateSerializer(
            tds,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ThanksDateSerializer(data=request.data)
        if serializer.is_valid():
            new_td = serializer.save(
                user=request.user,
            )
            serializer = ThanksDateSerializer(
                new_td,
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TD(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            td = ThanksDate.objects.get(pk=pk)
            return td
        except ThanksDate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        td = self.get_object(pk)
        serializer = ThanksDateSerializer(td)
        return Response(serializer.data)

    def put(self, request, pk):
        td = self.get_object(pk)
        if td.user != request.user:
            raise PermissionDenied
        serializer = ThanksDateSerializer(
            td,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_td = serializer.save()
            serializer = ThanksDateSerializer(
                updated_td,
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        td = self.get_object(pk)
        if td.user != request.user:
            raise PermissionDenied
        td.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Tks(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            thanksDate = ThanksDate.objects.get(pk=pk)
            return thanksDate
        except thanksDate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        thanksDate = self.get_object(pk)
        serializer = ThanksSerializer(
            thanksDate.thanks.all(),
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ThanksSerializer(data=request.data)
        if serializer.is_valid():
            new_thank = serializer.save(
                user=request.user,
                thanksDate=self.get_object(pk),
            )
            serializer = ThanksSerializer(new_thank)

            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

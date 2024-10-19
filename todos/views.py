from .serializers import EverydaySerializer, PlanSerializer, TodoSerializer
from .models import Todo, Everyday, Plan
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT


# Create your views here.


class Todos(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return Response(None)
            todos = Todo.objects.filter(user=request.user)
            
            serializer = TodoSerializer(
                todos,
                many=True,
            )
            return Response(serializer.data)
        except Todo.DoesNotExist:
            raise NotFound

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            new_todo = serializer.save(user=request.user)
            serializer = TodoSerializer(new_todo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TodoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            return todo
        except Todo.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(
            todo,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_todo = serializer.save()
            serializer = TodoSerializer(updated_todo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        if todo.user != request.user:
            raise PermissionDenied
        todo.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class EveryDays(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
            everydays = Everyday.objects.filter(todo=todo)
            serializer = EverydaySerializer(
                everydays,
                many=True,
            )
            return Response(serializer.data)
        except Everyday.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        serializer = EverydaySerializer(data=request.data)
        if serializer.is_valid():
            new_everyday = serializer.save(user=request.user, todo=todo)
            serializer = EverydaySerializer(new_everyday)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class EveryDay(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, pk_):
        try:
            everyday = Everyday.objects.get(pk=pk_, todo__pk=pk)
            return everyday
        except Everyday.DoesNotExist:
            raise NotFound

    def get(self, request, pk, pk_):
        everyday = self.get_object(pk, pk_)
        serializer = EverydaySerializer(everyday)
        return Response(serializer.data)

    def put(self, request, pk, pk_):
        everyday = self.get_object(pk, pk_)
        serializer = EverydaySerializer(
            everyday,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_everyday = serializer.save()
            serializer = EverydaySerializer(
                updated_everyday,
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk, pk_):
        everyday = self.get_object(pk, pk_)
        if everyday.user != request.user:
            raise PermissionDenied
        everyday.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Plans(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
            try:
                todo = Todo.objects.get(pk=pk)
                plans = Plan.objects.filter(todo=todo)
                serializer = PlanSerializer(
                    plans,
                    many=True,
                )
                return Response(serializer.data)
            except Plan.DoesNotExist:
                raise NotFound
       

    def post(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            new_plan = serializer.save(user=request.user, todo=todo)
            serializer = PlanSerializer(new_plan)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PlanDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, pk_):
        try:
            plan = Plan.objects.get(pk=pk_, todo__pk=pk)
            return plan
        except Plan.DoesNotExist:
            raise NotFound

    def get(self, request, pk, pk_):
        plan = self.get_object(pk, pk_)
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, pk, pk_):
        plan = self.get_object(pk, pk_)
        serializer = PlanSerializer(
            plan,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_plan = serializer.save()
            serializer = PlanSerializer(
                updated_plan,
            )
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk, pk_):
        plan = self.get_object(pk, pk_)
        if plan.user != request.user:
            raise PermissionDenied
        plan.delete()
        return Response(status=HTTP_204_NO_CONTENT)

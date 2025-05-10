from rest_framework import generics, permissions, viewsets
from .models import Habit
from .serializers import HabitSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .storage import upload_to_yandex_storage

User = get_user_model()

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=200)

class HabitViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        file = self.request.FILES.get('attachment')
        if file:
            url = upload_to_yandex_storage(file, f"habits/{file.name}")
            serializer.save(user=self.request.user, attachment=url)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
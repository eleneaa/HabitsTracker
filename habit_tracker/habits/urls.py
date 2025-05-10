from django.urls import path
from .views import HabitListCreateView, HabitRetrieveUpdateDestroyView, RegisterView, HealthCheckView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
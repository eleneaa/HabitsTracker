from django.urls import path, include
from .views import HabitListView, HabitCreateView, HabitUpdateView, HabitDeleteView, SignUpView
from django.urls import reverse_lazy
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

LOGIN_REDIRECT_URL = reverse_lazy('habit-list')
LOGOUT_REDIRECT_URL = reverse_lazy('login')

urlpatterns = [
    path('', HabitListView.as_view(), name='habit-list'),
    path('create/', HabitCreateView.as_view(), name='habit-create'),
    path('<int:pk>/edit/', HabitUpdateView.as_view(), name='habit-edit'),
    path('<int:pk>/delete/', HabitDeleteView.as_view(), name='habit-delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('health/', health_check),
]

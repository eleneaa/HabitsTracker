from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Habit
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import HabitForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'habits/habit_list.html'

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habits/habit_form.html'
    success_url = reverse_lazy('habit-list')

    def form_valid(self, form):
        file = self.request.FILES.get('attachment')
        if file:
            from .storage import upload_to_yandex_storage
            url = upload_to_yandex_storage(file, f"habits/{file.name}")
            form.instance.attachment = url
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habits/habit_form.html'
    success_url = reverse_lazy('habit-list')

    def form_valid(self, form):
        file = self.request.FILES.get('attachment')
        if file:
            from .storage import upload_to_yandex_storage
            url = upload_to_yandex_storage(file, f"habits/{file.name}")
            form.instance.attachment = url
        return super().form_valid(form)


class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    template_name = 'habits/habit_confirm_delete.html'
    success_url = reverse_lazy('habit-list')

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DesignRequest
def index(request):
    return render(request, 'index.html')

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

class RequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = DesignRequest
    fields = ['title', 'description']
    template_name = 'accounts/request_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RequestListView(LoginRequiredMixin, generic.ListView):
    model = DesignRequest
    template_name = 'accounts/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user)

class RequestDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DesignRequest
    template_name = 'accounts/request_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user)

# Create your views here.

from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .forms import RegistrationForm, DesignRequestForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import DesignRequest, Category

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# 1. Список всех заявок для админа
class AdminRequestListView(AdminRequiredMixin, generic.ListView):
    model = DesignRequest
    template_name = 'accounts/admin_requests.html'
    context_object_name = 'requests'
    ordering = ['-created']

# 2. Смена статуса заявки админом
class AdminRequestUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = DesignRequest
    fields = ['status', 'design_image']  # добавьте поле комментария, если оно есть в модели
    template_name = 'accounts/admin_request_edit.html'
    success_url = reverse_lazy('admin_requests')

# 3. Управление категориями (список + создание)
class AdminCategoryListView(AdminRequiredMixin, generic.CreateView):
    model = Category
    fields = ['name']
    template_name = 'accounts/admin_categories.html'
    success_url = reverse_lazy('admin_categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# 4. Удаление категории
class AdminCategoryDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Category
    template_name = 'accounts/admin_category_confirm_delete.html'
    success_url = reverse_lazy('admin_categories')
def index(request):
    completed_requests = DesignRequest.objects.filter(status='done').order_by('-created')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'index.html',
                  {'completed_requests': completed_requests, 'in_progress_count': in_progress_count})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['full_name'],
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else:
            form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

class RegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

class RequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = DesignRequest
    form_class = DesignRequestForm
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
        queryset = DesignRequest.objects.filter(user=self.request.user).order_by('-created')
        status = self.request.GET.get('status')
        if status in ['new', 'in_progress', 'done']:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        return context

class RequestDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DesignRequest
    template_name = 'accounts/request_confirm_delete.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return DesignRequest.objects.filter(user=self.request.user, status='new')

# Create your views here.

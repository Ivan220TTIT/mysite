from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('requests', views.RequestListView.as_view(), name='request_list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/', views.RequestDeleteView.as_view(), name='request_delete'),
    path('register/', views.register, name='register'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('requests', views.RequestListView.as_view(), name='request_list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/', views.RequestDeleteView.as_view(), name='request_delete'),
    path('register/', views.register, name='register'),
    path('superadmin/requests/', views.AdminRequestListView.as_view(), name='admin_requests'),
    path('superadmin/requests/<int:pk>/edit/', views.AdminRequestUpdateView.as_view(), name='admin_request_edit'),
    path('superadmin/categories/', views.AdminCategoryListView.as_view(), name='admin_categories'),
    path('superadmin/categories/<int:pk>/delete/', views.AdminCategoryDeleteView.as_view(), name='admin_category_delete'),
]

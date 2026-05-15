from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/api/update_registration/<int:reg_id>/', views.api_update_registration, name='api_update_registration'),
    path('dashboard/api/delete_registration/<int:reg_id>/', views.api_delete_registration, name='api_delete_registration'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('apply/<int:pk>/', views.job_apply, name='job_apply'),

    path('search/', views.search_jobs, name='search'),

]

from django.urls import path
from .views import delete_response, edit_response, signup, login, dashboard, surveyform, success, datatab
from myapp import views
from django.shortcuts import render
# from .views import index
# from .views import base

def success_view(request):
    return render(request, 'success.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def datatab_view(request):
    return(request, 'datatab.html')

def viewform_view(request):
    return(request, 'viewform.html')

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path('surveyform/', surveyform, name='surveyform'),
    path('success/', success, name='success'),
    path('datatab/', datatab, name='datatab'),
    path('viewform/', views.viewform, name='viewform'),
    path('edit/<str:response_id>/', edit_response, name='edit_response'),
    path('delete/<str:response_id>/', delete_response, name='delete_response'),
    # path("", index, name="index"),
    # path("", base, name="base"),
]
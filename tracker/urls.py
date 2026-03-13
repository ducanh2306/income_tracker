from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('register/', views.register, name='register'),
    path('add-expense/', views.add_expense, name='add_expense'),

]
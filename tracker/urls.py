from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),
    path('register/', views.register, name='register'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path("income-list/", views.income_list, name="income_list"),
    path("expense-list/", views.expense_list, name="expense_list"),
    path("income/edit/<int:pk>/", views.edit_income, name="edit_income"),
    path("income/delete/<int:pk>/", views.delete_income, name="delete_income"),

    path("expense/edit/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("expense/delete/<int:pk>/", views.delete_expense, name="delete_expense"),

]
from django import forms
from .models import Income, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount','source','date']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','category','date','description']
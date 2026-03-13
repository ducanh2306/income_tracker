from django.db.models import Sum

# Create your views here.
from django.shortcuts import render, redirect
from .models import Income, Expense
from .forms import IncomeForm, RegisterForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, login
from django.contrib import messages

@login_required
def dashboard(request):

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    savings = total_income - total_expense

    recent_incomes = incomes.order_by('-created_at')[:5]
    recent_expenses = expenses.order_by('-created_at')[:5]

    category_data = (
        expenses.values("category")
        .annotate(total=Sum("amount"))
    )

    categories = [item["category"] for item in category_data]
    category_totals = [float(item["total"]) for item in category_data]

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "recent_incomes": recent_incomes,
        "recent_expenses": recent_expenses,
        "categories": categories,
        "category_totals": category_totals
    }

    return render(request, "dashboard.html", context)

def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income =form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("dashboard")
    else:
        form = IncomeForm()

    return render(request, "add_income.html", {"form": form})

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("dashboard")
    else:
        form = ExpenseForm()
    return render(request, "add_expense.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Income, Expense, Budget
from .forms import IncomeForm, RegisterForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum
from datetime import datetime
from django.core.paginator import Paginator
@login_required
def dashboard(request):

    # Get user data FIRST
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Totals
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    savings = total_income - total_expense

    # ======================
    # 50/30/20 RULE
    # ======================

    NEED_CATEGORIES = [
        "Groceries", "Utilities", "Healthcare",
        "Insurance", "Rent", "Transportation"
    ]

    WANT_CATEGORIES = [
        "Dining Out", "Entertainment", "Education"
    ]

    need_expense = expenses.filter(category__in=NEED_CATEGORIES)\
        .aggregate(Sum("amount"))["amount__sum"] or 0

    want_expense = expenses.filter(category__in=WANT_CATEGORIES)\
        .aggregate(Sum("amount"))["amount__sum"] or 0

    need_percent = (need_expense / total_income * 100) if total_income > 0 else 0
    want_percent = (want_expense / total_income * 100) if total_income > 0 else 0

    warnings = []

    if need_percent > 50:
        warnings.append("⚠ You are spending over 50% for need!!")

    if want_percent > 30:
        warnings.append("⚠ You are spending over 30% for want!!")

    # ======================
    # DAILY SPENDING WARNING
    # ======================

    today = now().date()

    today_expense = expenses.filter(date=today)\
        .aggregate(Sum('amount'))['amount__sum'] or 0

    last_7_days = expenses.filter(date__gte=today - timedelta(days=7))

    avg_daily = 0
    if last_7_days.exists():
        avg_daily = (last_7_days.aggregate(Sum('amount'))['amount__sum'] or 0) / 7

    if avg_daily > 0 and today_expense > avg_daily * 2:
        warnings.append("⚠ You are spending unusually high today!")

    # ======================
    # RECENT TRANSACTIONS
    # ======================

    recent_incomes = incomes.order_by('-created_at')[:5]
    recent_expenses = expenses.order_by('-created_at')[:5]

    # ======================
    # CATEGORY CHART
    # ======================

    category_data = expenses.values("category").annotate(total=Sum("amount"))

    categories = [item["category"] for item in category_data]
    category_totals = [float(item["total"]) for item in category_data]

    # ======================
    # CONTEXT
    # ======================

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,

        "recent_incomes": recent_incomes,
        "recent_expenses": recent_expenses,

        "categories": categories,
        "category_totals": category_totals,

        "need_expense": need_expense,
        "want_expense": want_expense,
        "need_percent": need_percent,
        "want_percent": want_percent,

        "warnings": warnings
    }

    return render(request, "dashboard.html", context)

@login_required
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

@login_required
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

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(incomes, 5)   # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "income_list.html", {"page_obj": page_obj})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "expense_list.html", {
        "page_obj": page_obj
    })

@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)

    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = IncomeForm(instance=income)

    return render(request, "add_income.html", {"form": form})

@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    income.delete()
    return redirect("dashboard")

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "add_expense.html", {"form": form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect("dashboard")

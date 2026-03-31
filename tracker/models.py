from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Income(models.Model):
    CATEGORY_CHOICES = [
        ("Salary", "Salary"),
        ("Freelancer", "Freelancer"),
        ("Mixed", "Mixed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Groceries", "Groceries"),
        ("Utilities", "Utilities"),
        ("Healthcare", "Healthcare"),
        ("Insurance", "Insurance"),
        ("Rent", "Rent"),
        ("Transportation", "Transportation"),
        ("Dining Out", "Dining Out"),
        ("Entertainment", "Entertainment"),
        ("Education", "Education"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_goal = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    def __str__(self):
        return f"{self.user.username} goal"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"
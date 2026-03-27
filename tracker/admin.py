from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Income, Expense, Goal

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount','source' ,'date')
    list_filter = ('date','source')
    search_fields = ('user__username','source')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user','category', 'amount','date')
    list_filter = ('date','category')
    search_fields = ('user__username','category')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_goal')
    search_fields = ('user__username',)


#admin.site.register(Income, IncomeAdmin)
#admin.site.register(Income)
#admin.site.register(Expense)
#admin.site.register(Goal)
from django.contrib import admin

from .models import History


@admin.register(History)
# Register your models here.

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'return_date', 'returned', 'amount', 'balance_after_borrow', 'balance_after_return', 'history_type']
    

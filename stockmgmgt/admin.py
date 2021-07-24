from django.contrib import admin
from .forms import StockCreateForm

# Register your models here.

from .models import Stock

class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity', 'issue_by', 'price']
    form = StockCreateForm
    list_filter = ['item_name']
    search_fields = ['item_name']

admin.site.register(Stock, StockCreateAdmin)
from django.contrib import admin

# Register your models here.
from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["id","user","institution_name"]
    list_display_links =["id","user"]
    list_filter = ["institution_name"]
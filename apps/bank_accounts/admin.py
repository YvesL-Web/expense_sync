from django.contrib import admin

# Register your models here.
from .models import BankAccount, SyncCursor, Transaction

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["id","user","institution_name"]
    list_display_links =["id","user"]
    list_filter = ["institution_name"]


@admin.register(SyncCursor)
class SyncCursorAdmin(admin.ModelAdmin):
    list_display = ["id","bank","cursor"]
    list_display_links =["id","bank"]
    list_filter = ["bank"]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id","bank","name","amount","date"]
    list_display_links =["id","bank"]
    list_filter = ["bank","date"]
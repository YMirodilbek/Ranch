from django.contrib import admin

# Register your models here.
from .models import Transactions

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount'

    )
    list_filter=("user",)
    search_fields = ('id','user')
admin.site.register(Transactions,TransactionAdmin)
from django.contrib import admin
from .models import ystu_account
# Register your models here.
#admin.site.register(ystu_account)

@admin.register(ystu_account)
class profileAdmin(admin.ModelAdmin):
    list_display = ('username_django', 'login', 'full_name')
from django.contrib import admin
from .models import is_beta
# Register your models here.
@admin.register(is_beta)
class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'beta')
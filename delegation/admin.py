from django.contrib import admin
from .models import team, list_members_teams, messages, ConditionTask, ResultTask, Tasks
# Register your models here.

admin.site.register(team)


@admin.register(list_members_teams)
class profileAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user')


@admin.register(messages)
class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_create')

@admin.register(ConditionTask)
class profileAdmin(admin.ModelAdmin):
    list_display = ('condition', )

@admin.register(ResultTask)
class profileAdmin(admin.ModelAdmin):
    list_display = ('typeResult', )

@admin.register(Tasks)
class profileAdmin(admin.ModelAdmin):
    list_display = ('nameTask', 'currentDate', 'condition', 'typeResult', 'dueDate')
from django.contrib import admin

from .models import Objective, Goal


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 3


class ObjectiveAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['metric_name', 'description']})]
    inlines = [GoalInline]


admin.site.register(Objective, ObjectiveAdmin)

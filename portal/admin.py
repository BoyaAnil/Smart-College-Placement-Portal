from django.contrib import admin

from .models import Application, Job, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "branch", "cgpa")
    search_fields = ("user__username", "user__email", "branch")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "recruiter", "location", "last_date")
    search_fields = ("title", "company", "location")
    list_filter = ("job_type", "location")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "student", "status", "created_at")
    list_filter = ("status",)

from django.contrib import admin
from .models import Project, Finding, FindingLibrary, FindingAttachment


class FindingInline(admin.TabularInline):
    model = Finding
    extra = 0
    fields = ["title", "severity", "status", "cvss_score"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project_name", "client_name", "project_type", "status", "owner", "created_at"]
    list_filter = ["status", "project_type"]
    search_fields = ["client_name", "project_name"]
    inlines = [FindingInline]


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ["title", "severity", "status", "cvss_score", "project", "created_at"]
    list_filter = ["severity", "status"]
    search_fields = ["title", "description"]


@admin.register(FindingLibrary)
class FindingLibraryAdmin(admin.ModelAdmin):
    list_display = ["title", "severity", "cvss_score", "created_by"]
    list_filter = ["severity"]
    search_fields = ["title"]

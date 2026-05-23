import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        IN_PROGRESS = "in_progress", "In Progress"
        REVIEW = "review", "Review"
        COMPLETED = "completed", "Completed"
        ARCHIVED = "archived", "Archived"

    class ProjectType(models.TextChoices):
        EXTERNAL = "external", "External Pentest"
        INTERNAL = "internal", "Internal Pentest"
        WEB = "web", "Web Application"
        MOBILE = "mobile", "Mobile Application"
        SOCIAL = "social", "Social Engineering"
        PHYSICAL = "physical", "Physical"
        RED_TEAM = "red_team", "Red Team"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50, choices=ProjectType.choices, default=ProjectType.WEB)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    scope = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_projects")
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.project_name}"

    def get_findings_stats(self):
        counts = {s: 0 for s in Finding.Severity.values}
        for finding in self.findings.values("severity").iterator():
            counts[finding["severity"]] += 1
        return counts


class Finding(models.Model):
    class Severity(models.TextChoices):
        CRITICAL = "critical", "Critical"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"
        INFO = "info", "Informational"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_REVIEW = "in_review", "In Review"
        RESOLVED = "resolved", "Resolved"
        ACCEPTED = "accepted", "Risk Accepted"
        FALSE_POSITIVE = "false_positive", "False Positive"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="findings")
    title = models.CharField(max_length=500)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    cvss_vector = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    remediation = models.TextField(blank=True)
    steps_to_reproduce = models.TextField(blank=True)
    affected_components = models.TextField(blank=True)
    references = models.JSONField(default=list, blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="findings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-severity", "-created_at"]

    def __str__(self):
        return f"[{self.severity.upper()}] {self.title}"


class FindingAttachment(models.Model):
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="findings/attachments/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class FindingLibrary(models.Model):
    """Reusable finding templates across projects."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    severity = models.CharField(max_length=20, choices=Finding.Severity.choices, default=Finding.Severity.MEDIUM)
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    cvss_vector = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    remediation = models.TextField(blank=True)
    references = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Finding Library"
        ordering = ["title"]

    def __str__(self):
        return self.title

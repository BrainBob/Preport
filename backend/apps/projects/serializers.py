from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Project, Finding, FindingAttachment, FindingLibrary


class FindingAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingAttachment
        fields = ["id", "file", "caption", "uploaded_at"]


class FindingSerializer(serializers.ModelSerializer):
    attachments = FindingAttachmentSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Finding
        fields = [
            "id", "project", "title", "severity", "status",
            "cvss_score", "cvss_vector", "description", "impact",
            "remediation", "steps_to_reproduce", "affected_components",
            "references", "custom_fields", "order", "attachments",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class FindingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ["id", "title", "severity", "status", "cvss_score", "order", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    team_members = UserSerializer(many=True, read_only=True)
    team_member_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=__import__("apps.accounts.models", fromlist=["User"]).User.objects.all(),
        source="team_members", required=False,
    )
    findings_stats = serializers.SerializerMethodField()
    findings_count = serializers.IntegerField(source="findings.count", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "client_name", "project_name", "project_type", "status",
            "start_date", "end_date", "scope", "notes",
            "owner", "team_members", "team_member_ids",
            "findings_stats", "findings_count",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def get_findings_stats(self, obj):
        return obj.get_findings_stats()

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class FindingLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingLibrary
        fields = [
            "id", "title", "severity", "cvss_score", "cvss_vector",
            "description", "impact", "remediation", "references",
            "created_by", "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

from rest_framework import serializers
from .models import ReportTemplate, Section, Report


class SectionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["id", "title", "content", "order", "parent", "children"]

    def get_children(self, obj):
        return SectionSerializer(obj.children.all(), many=True).data


class ReportTemplateSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = ReportTemplate
        fields = [
            "id", "name", "description", "css_styles",
            "header_template", "footer_template", "finding_template",
            "is_default", "sections", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id", "project", "template", "title",
            "included_findings", "generated_pdf", "status",
            "error_message", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "generated_pdf", "status", "error_message", "created_at", "updated_at"]

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ReportTemplate, Section, Report
from .serializers import ReportTemplateSerializer, SectionSerializer, ReportSerializer


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer

    @action(detail=True, methods=["post"])
    def clone(self, request, pk=None):
        template = self.get_object()
        sections = list(template.sections.all())

        template.pk = None
        template.name = f"{template.name} (Copy)"
        template.is_default = False
        template.save()

        for section in sections:
            section.pk = None
            section.report_template = template
            section.save()

        return Response(ReportTemplateSerializer(template).data, status=status.HTTP_201_CREATED)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.user
        return Report.objects.filter(project__owner=user) | Report.objects.filter(project__team_members=user)

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        report = self.get_object()
        from apps.pdf.services import PDFGenerationService
        service = PDFGenerationService(report)
        service.generate()
        report.refresh_from_db()
        return Response(ReportSerializer(report).data)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        from django.http import FileResponse
        report = self.get_object()
        if not report.generated_pdf:
            return Response({"detail": "PDF not generated yet."}, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(report.generated_pdf.open("rb"), content_type="application/pdf")

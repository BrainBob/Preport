from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.reports.models import Report
from .services import PDFGenerationService


class GeneratePDFView(APIView):
    def post(self, request, report_id):
        try:
            report = Report.objects.get(pk=report_id, project__owner=request.user)
        except Report.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        service = PDFGenerationService(report)
        service.generate()
        report.refresh_from_db()

        return Response({
            "status": report.status,
            "pdf_url": request.build_absolute_uri(report.generated_pdf.url) if report.generated_pdf else None,
            "error": report.error_message or None,
        })

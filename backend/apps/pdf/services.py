import io
import markdown
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML, CSS


SEVERITY_COLORS = {
    "critical": "#FF0000",
    "high": "#FF6B00",
    "medium": "#FFD700",
    "low": "#00C853",
    "info": "#2196F3",
}


class PDFGenerationService:
    def __init__(self, report):
        self.report = report

    def generate(self):
        from apps.reports.models import Report
        self.report.status = Report.Status.GENERATING
        self.report.save(update_fields=["status"])

        try:
            html_content = self._render_html()
            pdf_bytes = self._render_pdf(html_content)

            filename = f"report_{self.report.id}.pdf"
            self.report.generated_pdf.save(filename, ContentFile(pdf_bytes), save=False)
            self.report.status = Report.Status.READY
            self.report.error_message = ""
        except Exception as exc:
            self.report.status = Report.Status.FAILED
            self.report.error_message = str(exc)

        self.report.save(update_fields=["generated_pdf", "status", "error_message"])

    def _render_html(self):
        report = self.report
        project = report.project
        template = report.template

        findings = report.included_findings.all().order_by("order", "severity")

        processed_findings = []
        for f in findings:
            processed_findings.append({
                "obj": f,
                "description_html": markdown.markdown(f.description or ""),
                "impact_html": markdown.markdown(f.impact or ""),
                "remediation_html": markdown.markdown(f.remediation or ""),
                "steps_html": markdown.markdown(f.steps_to_reproduce or ""),
                "color": SEVERITY_COLORS.get(f.severity, "#000"),
            })

        context = {
            "report": report,
            "project": project,
            "template": template,
            "findings": processed_findings,
            "severity_colors": SEVERITY_COLORS,
        }

        css_override = ""
        if template and template.css_styles:
            css_override = template.css_styles

        return render_to_string("pdf/report.html", context), css_override

    def _render_pdf(self, html_and_css):
        html_content, css_override = html_and_css
        html = HTML(string=html_content, base_url="")
        stylesheets = []
        if css_override:
            stylesheets.append(CSS(string=css_override))
        pdf = html.write_pdf(stylesheets=stylesheets or None)
        return pdf

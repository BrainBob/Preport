from django.urls import path
from .views import GeneratePDFView

urlpatterns = [
    path("generate/<uuid:report_id>/", GeneratePDFView.as_view(), name="generate-pdf"),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportTemplateViewSet, ReportViewSet

router = DefaultRouter()
router.register("templates", ReportTemplateViewSet, basename="template")
router.register("", ReportViewSet, basename="report")

urlpatterns = [
    path("", include(router.urls)),
]

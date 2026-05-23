from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, FindingViewSet, FindingAttachmentViewSet, FindingLibraryViewSet

router = DefaultRouter()
router.register("", ProjectViewSet, basename="project")
router.register("findings", FindingViewSet, basename="finding")
router.register("library", FindingLibraryViewSet, basename="finding-library")

urlpatterns = [
    path("", include(router.urls)),
]

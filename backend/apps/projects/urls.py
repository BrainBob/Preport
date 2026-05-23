from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, FindingViewSet, FindingLibraryViewSet

projects_router = DefaultRouter()
projects_router.register("", ProjectViewSet, basename="project")

findings_router = DefaultRouter()
findings_router.register("", FindingViewSet, basename="finding")

library_router = DefaultRouter()
library_router.register("", FindingLibraryViewSet, basename="finding-library")

# findings/ and library/ must come before "" to avoid "" eating them as project PKs
urlpatterns = [
    path("findings/", include(findings_router.urls)),
    path("library/", include(library_router.urls)),
    path("", include(projects_router.urls)),
]

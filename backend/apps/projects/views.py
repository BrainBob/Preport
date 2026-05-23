from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, Finding, FindingAttachment, FindingLibrary
from .serializers import (
    ProjectSerializer, FindingSerializer, FindingListSerializer,
    FindingAttachmentSerializer, FindingLibrarySerializer,
)
from .permissions import IsOwnerOrTeamMember, IsProjectOwner


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "project_type"]
    search_fields = ["client_name", "project_name"]
    ordering_fields = ["created_at", "client_name", "status"]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(team_members=user)
        ).distinct().order_by("-created_at")

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsProjectOwner()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def clone(self, request, pk=None):
        project = self.get_object()
        findings = list(project.findings.all())

        project.pk = None
        project.project_name = f"{project.project_name} (Copy)"
        project.status = Project.Status.PLANNING
        project.owner = request.user
        project.save()

        for finding in findings:
            finding.pk = None
            finding.project = project
            finding.save()

        return Response(ProjectSerializer(project, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        project = self.get_object()
        data = ProjectSerializer(project, context={"request": request}).data
        data["findings"] = FindingSerializer(project.findings.all(), many=True, context={"request": request}).data
        return Response(data)


class FindingViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["severity", "status", "project"]
    search_fields = ["title", "affected_components", "description"]
    ordering_fields = ["severity", "cvss_score", "order", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return FindingListSerializer
        return FindingSerializer

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs.get("project_pk") or self.request.query_params.get("project")
        qs = Finding.objects.filter(
            project__owner=user
        ) | Finding.objects.filter(project__team_members=user)
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs.distinct()

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        serializer = FindingSerializer(data=request.data, many=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_to_library(self, request, pk=None):
        finding = self.get_object()
        library_item = FindingLibrary.objects.create(
            title=finding.title,
            severity=finding.severity,
            cvss_score=finding.cvss_score,
            cvss_vector=finding.cvss_vector,
            description=finding.description,
            impact=finding.impact,
            remediation=finding.remediation,
            references=finding.references,
            created_by=request.user,
        )
        return Response(FindingLibrarySerializer(library_item).data, status=status.HTTP_201_CREATED)


class FindingAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = FindingAttachmentSerializer

    def get_queryset(self):
        return FindingAttachment.objects.filter(finding_id=self.kwargs["finding_pk"])

    def perform_create(self, serializer):
        finding = get_object_or_404(Finding, pk=self.kwargs["finding_pk"])
        serializer.save(finding=finding)


class FindingLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = FindingLibrarySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["severity"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return FindingLibrary.objects.all()

    @action(detail=True, methods=["post"])
    def use_in_project(self, request, pk=None):
        library_item = self.get_object()
        project_id = request.data.get("project_id")
        project = get_object_or_404(Project, pk=project_id)

        finding = Finding.objects.create(
            project=project,
            title=library_item.title,
            severity=library_item.severity,
            cvss_score=library_item.cvss_score,
            cvss_vector=library_item.cvss_vector,
            description=library_item.description,
            impact=library_item.impact,
            remediation=library_item.remediation,
            references=library_item.references,
            created_by=request.user,
        )
        return Response(FindingSerializer(finding, context={"request": request}).data, status=status.HTTP_201_CREATED)

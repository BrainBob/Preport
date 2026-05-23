# Preport — Progress Tracker

## Phase 1 — Backend Skeleton ✅ (done 2026-05-23)

### Backend
- [x] Django project structure (`config/settings/base.py`, `dev.py`)
- [x] Custom User model (`accounts.User`, email as USERNAME_FIELD)
- [x] Models: `Project`, `Finding`, `FindingAttachment`, `FindingLibrary`
- [x] Models: `ReportTemplate`, `Section` (self-referential), `Report`
- [x] DRF serializers for all apps
- [x] ViewSets: ProjectViewSet (clone, export), FindingViewSet (bulk_create, add_to_library)
- [x] ViewSets: ReportViewSet (generate, download), ReportTemplateViewSet (clone)
- [x] Custom permissions: `IsOwnerOrTeamMember`, `IsProjectOwner`
- [x] JWT auth: simplejwt (1h access / 7d refresh with rotation)
- [x] PDF generation: `PDFGenerationService` + WeasyPrint + `report.html` template
- [x] Swagger/OpenAPI: drf-spectacular at `/api/docs/`
- [x] URL routing for all apps

### Infrastructure
- [x] Docker Compose: db, backend, frontend, nginx
- [x] Backend Dockerfile (python:3.12-slim + WeasyPrint system deps)
- [x] Frontend Dockerfile (node:20-alpine)
- [x] Nginx reverse proxy (WebSocket upgrade for Vite HMR)
- [x] `.env.example` with all required vars
- [x] `Makefile` (build, up, down, migrate, seed, lint)
- [x] `.pre-commit-config.yaml` (black, flake8, pre-commit-hooks)
- [x] `.gitignore`
- [x] Push to `https://github.com/BrainBob/Preport.git` (commit 2973477)

---

## Phase 2 — Frontend Views 🔄 (in progress 2026-05-23)

### Infrastructure
- [x] `frontend/index.html` — Vite entry point
- [x] `frontend/tailwind.config.js` + `postcss.config.js`
- [x] Pinia stores: `auth.js`, `projects.js`

### Stores (new)
- [x] `stores/findings.js`
- [x] `stores/reports.js`
- [x] `stores/templates.js`
- [x] `stores/library.js`

### Views
- [x] Router (`router/index.js`) — all routes + beforeEach guard
- [x] `LoginView.vue` — email/password form, redirect on success
- [x] `AppLayout.vue` — sidebar nav + RouterView
- [x] `ProjectsView.vue` — card grid, filters, create dialog
- [x] `ProjectDetailView.vue` — project header + findings table + delete confirm
- [x] `FindingEditorView.vue` — Tiptap rich text per field + CVSS + status + references
- [x] `ReportsView.vue` — reports list + generate + download PDF
- [x] `TemplatesView.vue` — template list + create/edit/clone/delete
- [x] `LibraryView.vue` — library findings + use-in-project dialog

### Components
- [x] `SeverityBadge.vue`
- [x] `ProjectCard.vue` — card with severity counts + status chip
- [x] `RichTextSection.vue` — Tiptap editor panel with toolbar (bold/italic/code/list)
- [ ] `CvssCalculator.vue` (Phase 3)

---

## Phase 3 — Integration & Testing

- [ ] `make build && make up && make migrate` — verify stack starts
- [ ] `make createsuperuser` — first admin user
- [ ] `seed_data.py` management command (3 projects, 15+ findings, 2 templates)
- [ ] End-to-end: login → create project → add finding → generate PDF
- [ ] Fix any import/migration errors found during first run
- [ ] Backend unit tests (pytest-django) for serializers + views
- [ ] Frontend Vitest unit tests for stores

---

## Phase 4 — Advanced Features

- [ ] Tiptap rich text editor in FindingEditorView (bold, italic, code, images)
- [ ] Drag-drop screenshot upload in FindingEditor (`FindingAttachment`)
- [ ] CVSS v3.1 calculator component (interactive vector builder)
- [ ] Drag-drop finding reordering (vuedraggable) in ProjectDetailView
- [ ] Report section drag-drop builder in TemplatesView
- [ ] PDF preview (iframe, full-screen) in ReportsView
- [ ] Finding import from library (bulk add to project)
- [ ] Project export → JSON + re-import
- [ ] Dark mode toggle
- [ ] User profile page (avatar upload, bio)

---

## Known Decisions / Notes

| Decision | Reason |
|---|---|
| UUID PKs on main models | Avoid sequential ID enumeration in URLs |
| WeasyPrint server-side PDF | No browser dependency, reproducible output |
| PrimeVue 4 + Tailwind | Rich component set + utility styling |
| JWT rotate on refresh | Security: refresh token single-use |
| flake8 max-line-length=120 | Black default is 88 but Django code is verbose |
| gunicorn --reload in dev | Hot-reload without rebuilding container |

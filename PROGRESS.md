# Preport — Progress Tracker

---

## Phase 1 — Backend Skeleton ✅ (2026-05-23)

- [x] Django 4.2 + DRF + simplejwt + drf-spectacular
- [x] Custom User model (email as login)
- [x] Models: Project, Finding, FindingAttachment, FindingLibrary, ReportTemplate, Section, Report
- [x] ViewSets с actions: clone, export, bulk_create, add_to_library, generate PDF, download
- [x] Permissions: IsOwnerOrTeamMember, IsProjectOwner
- [x] WeasyPrint PDF generation + HTML template (A4, cover page, ToC, findings)
- [x] Docker Compose: db + backend + frontend + nginx
- [x] Makefile, .env.example, .pre-commit-config.yaml, .gitignore

---

## Phase 2 — Frontend ✅ (2026-05-23)

- [x] Vite + Vue 3 + Pinia + PrimeVue 4 (Aura) + Tailwind
- [x] Axios client с JWT auto-refresh interceptor
- [x] Stores: auth, projects, findings, reports, templates, library
- [x] Views: Login, AppLayout (sidebar), Projects, ProjectDetail, FindingEditor, Reports, Templates, Library
- [x] Components: SeverityBadge, ProjectCard, RichTextSection (Tiptap)
- [x] Router с beforeEach auth guard

---

## Phase 3 — Stack Running ✅ (2026-05-23)

- [x] Docker stack запущен: все 4 контейнера Up
- [x] Миграции применены (accounts, projects, reports)
- [x] Seed data: 3 проекта, 15 findings, 2 шаблона, 5 library items
- [x] Логин работает, JWT выдаётся
- [x] Все API эндпоинты проверены (projects, findings, library, templates, reports)
- [x] Фикс: `union()` → `Q(owner|team_members).distinct()` в ProjectViewSet
- [x] Фикс: URL routing — findings/library router объявлен до пустого prefix
- [x] Фикс: POSTGRES_* переменные переданы в backend контейнер
- [x] Фикс: DataTable белый фон (override Aura dark surface)
- [x] UI открывается в браузере, данные отображаются

---

## Phase 4 — UI Polish & Core UX 🔄 (следующее)

### Срочно (мелкие баги)
- [ ] ProjectsView: карточки проектов не показывают findings_stats (нет поля в сериализаторе)
- [ ] Finding Editor: клик по строке → открытие редактора (проверить)
- [ ] Finding Editor: сохранение через кнопку Save работает?

### PDF генерация (ключевая фича)
- [ ] Создать Report через ReportsView → Generate PDF → Download
- [ ] Проверить WeasyPrint работает в контейнере (системные шрифты)
- [ ] PDF preview: iframe внутри приложения

### Rich text & редактор
- [ ] Tiptap: проверить что редактор рендерится и сохраняет HTML
- [ ] Drag-drop сортировка findings (vuedraggable)
- [ ] Drag-drop загрузка скриншотов в finding (FindingAttachment)

### CVSS Calculator
- [ ] Интерактивный калькулятор CVSS 3.1 (выбор векторов → автосчёт score)

---

## Phase 5 — Advanced Features

- [ ] Template builder: drag-drop секции, редактирование finding_template HTML
- [ ] Finding library: bulk import в проект (несколько findings за раз)
- [ ] Project import: загрузить JSON из export обратно
- [ ] User profile: аватар, bio, смена пароля
- [ ] Team members: добавить/убрать из проекта

---

## Phase 6 — Production

- [ ] Django settings prod (DEBUG=False, ALLOWED_HOSTS, CSRF)
- [ ] Nginx prod config (gzip, cache headers, SSL/TLS)
- [ ] Gunicorn без --reload, workers = 2*CPU+1
- [ ] Celery + Redis для async PDF generation
- [ ] Backup стратегия для postgres_data volume
- [ ] Деплой: VPS / Hetzner / fly.io

---

## Known Decisions

| Решение | Причина |
|---|---|
| UUID PKs | Нет IDOR через перебор числовых ID |
| WeasyPrint server-side | Воспроизводимый PDF без браузера |
| PrimeVue 4 + Tailwind | Богатые компоненты + утилитарный стиль |
| JWT rotate on refresh | Одноразовый refresh token |
| Q() вместо union() | union() не поддерживает .get()/.filter() после |
| findings/ до "" в router | Django URL resolver — первый совпавший паттерн |

Создай Django проект для системы отчетов пентестов (аналог SysReptor) со следующей структурой:

Модели:
1. Project (client_name, project_type, start_date, end_date, status, team_members)
2. Finding (project - FK, title, severity(Enum: Critical/High/Medium/Low/Info), cvss_score, description, impact, remediation, steps_to_reproduce, affected_components, references - JSON, custom_fields - JSON)
3. ReportTemplate (name, description, css_styles, header_template, footer_template, finding_template)
4. Section (report_template - FK, title, content, order, parent - FK self)
5. Report (project - FK, template - FK, generated_pdf, status, created_at)

API эндпоинты:
- CRUD для проектов с фильтрацией по статусу и клиенту
- CRUD для findings с bulk create/update
- Управление шаблонами отчетов
- Генерация PDF с выбором находок для включения
- Экспорт/импорт проектов (JSON)

Добавь:
- Кастомные permissions (только автор проекта может редактировать)
- API для клонирования проекта с находками
- Swagger документацию (drf-spectacular)
- Фильтрацию findings по severity, affected_component
- Возможность переиспользовать findings между проектами (FindingLibrary)

Напиши полный код models.py, serializers.py, views.py и urls.py.
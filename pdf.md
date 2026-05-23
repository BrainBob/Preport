Создай сервис генерации PDF отчетов на Django с WeasyPrint.

Требования:
1. HTML/CSS шаблоны отчетов с поддержкой:
   - Титульная страница (логотип компании, название проекта, дата, классификация)
   - Table of Contents с якорными ссылками
   - Колонтитулы (header/footer на каждой странице)
   - Цветовое кодирование severity (Critical=#FF0000, High=#FF6B00, Medium=#FFD700, Low=#00C853, Info=#2196F3)
   - Таблицы с находками (ID, Title, Severity, CVSS)
   - Детальные страницы для каждой находки
   - Поддержка Markdown в описаниях (конвертация в HTML)
   - Изображения/скриншоты в находках (base64 или URL)

2. Django management command для генерации отчета:
   - python manage.py generate_report --project-id=1 --template-id=1
   - Сохраняет PDF в FileField модели Report

3. CSS стили для печати:
   - @page с размерами A4
   - page-break правильное
   - Нумерация страниц "Страница X из Y"

Напиши полный код сервиса, шаблонов и management command.
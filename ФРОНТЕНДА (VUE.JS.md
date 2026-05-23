Создай Vue 3 приложение для интерфейса системы отчетов пентестов.

Ключевые компоненты:

1. ProjectDashboard:
   - Список проектов в виде карточек
   - Фильтры по статусу, поиск по клиенту
   - Быстрый просмотр статистики (кол-во находок по severity)
   - Кнопки: новый проект, клонировать, удалить

2. FindingEditor:
   - Rich text editor (Tiptap или Quill) для описания находок
   - Поля: title, severity select, CVSS калькулятор, описание, impact, remediation
   - Drag-and-drop для загрузки скриншотов
   - Markdown поддержка
   - Кнопка "Сохранить и создать следующий"

3. ReportTemplateBuilder:
   - WYSIWYG редактор структуры отчета
   - Drag-and-drop секций
   - Предпросмотр стилей

4. PDFPreview:
   - iframe предпросмотр сгенерированного HTML перед PDF
   - Выбор находок для включения в отчет чекбоксами

Используй:
- Pinia store для управления состоянием
- Vue Router с lazy loading
- Axios с перехватчиками для JWT
- Tailwind CSS для стилизации
- Компонентную библиотеку PrimeVue или Naive UI

Напиши код для ProjectDashboard.vue, FindingEditor.vue и stores.
from django.contrib import admin
from django.utils.html import format_html
from .models import Todo, Category

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_colored', 'colored_priority', 'category', 'due_date_display', 'is_completed')
    list_filter = ('is_completed', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_completed',)
    ordering = ('-created_at',)

    def title_colored(self, obj):
        if obj.is_completed:
            return format_html('<span style="background: #d4edda; padding:3px 6px; border-radius:4px;">✔ {}</span>', obj.title)
        elif obj.is_overdue():
            return format_html('<span style="background: #f8d7da; padding:3px 6px; border-radius:4px;">⚠ {}</span>', obj.title)
        return obj.title
    title_colored.short_description = "Title"

    def colored_priority(self, obj):
        colors = {'H': 'red', 'M': 'orange', 'L': 'green'}
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', colors.get(obj.priority, 'black'), obj.get_priority_display())
    colored_priority.short_description = "Priority"

    def due_date_display(self, obj):
        if obj.due_date and obj.is_overdue():
            return format_html('<span style="color:red; font-weight:bold;">{} (Overdue)</span>', obj.due_date)
        elif obj.due_date:
            return obj.due_date
        return "—"
    due_date_display.short_description = "Due Date"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

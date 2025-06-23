from django.contrib import admin
from .models import srexam

@admin.register(srexam)
class ipexamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_date', 'is_public', 'created_at')
    search_fields = ('name', 'students__email')
    list_filter = ('is_public', 'created_at', 'exam_date')
    filter_horizontal = ('students',)
    date_hierarchy = 'exam_date'

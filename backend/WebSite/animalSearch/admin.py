from django.contrib import admin
from django.db.models import Count
from .models import *
from django.utils.html import format_html_join
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponse
from io import BytesIO
from django.contrib.admin.actions import delete_selected
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Действие для генерации PDF

def generate_pdf(modeladmin, request, queryset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Путь к вашему TTF-шрифту
    font_path = os.path.join('static', 'fonts', 'DejaVuSans.ttf')

    # Регистрируем шрифт
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    # Используем шрифт
    p.setFont("DejaVuSans", 12)

    x = 50
    y = height - 50

    p.drawString(x, y, "ОТЧЕТ ОБ ОБЪЯВЛЕНИЯХ")
    y -= 30

    for report in queryset:
        p.drawString(x, y, f"Заголовок: {report.title}")
        y -= 20

        if report.description:
            p.drawString(x, y, f"Описание: {report.description}")
            y -= 20

        if y < 50:
            p.showPage()
            p.setFont("DejaVuSans", 12)
            y = height - 50

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
    return response

generate_pdf.short_description = _("Сгенерировать PDF для выбранных объявлений")


# Действие для перехода на сайт
def go_to_site(modeladmin, request, queryset):
    from django.shortcuts import redirect
    return redirect('/')  # Замените на нужный URL вашего сайта

go_to_site.short_description = _("Перейти на сайт")


class FavoriteReportsInline(admin.TabularInline):
    model = FavoriteReportItem
    extra = 1
    raw_id_fields = ('report',)
    verbose_name = "Избранное объявление"
    verbose_name_plural = "Избранные объявления"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone', 'date_joined', 'password_strength')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'email', 'phone')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined',)
    actions = [go_to_site]

    @admin.display(description="Сложность пароля", ordering="password")
    def password_strength(self, obj):
        return f"{len(obj.password)} символов"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_desc', 'post_date', 'display_picture')  # заменили has_picture на display_picture
    list_filter = ('post_date',)
    search_fields = ('title', 'short_desc', 'description')
    date_hierarchy = 'post_date'
    readonly_fields = ('post_date', 'display_picture_preview')  # для страницы редактирования
    actions = [go_to_site]

    @admin.display(description="Изображение")
    def display_picture(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.picture.url
            )
        return "Нет изображения"

    @admin.display(description="Превью изображения")
    def display_picture_preview(self, obj):
        return self.display_picture(obj)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'receiver_name', 'message_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender_id__first_name', 'receiver_id__first_name', 'text')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('sender_id', 'receiver_id')
    actions = [go_to_site]

    @admin.display(description="Отправитель")
    def sender_name(self, obj):
        return obj.sender_id.first_name if obj.sender_id else "Неизвестный отправитель"

    @admin.display(description="Получатель")
    def receiver_name(self, obj):
        return obj.receiver_id.first_name if obj.receiver_id else "Неизвестный получатель"

    @admin.display(description="Текст сообщения")
    def message_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'rating', 'review_preview', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('user_id__first_name', 'text')
    date_hierarchy = 'date'
    readonly_fields = ('date',)
    actions = [go_to_site]

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.first_name if obj.user_id else "—"

    @admin.display(description="Текст отзыва")
    def review_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'notification_preview', 'date', 'read_status')
    list_filter = ('read', 'date')
    search_fields = ('user_id__first_name', 'text')
    date_hierarchy = 'date'
    readonly_fields = ('date',)
    actions = [go_to_site]

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.first_name if obj.user_id else "—"

    @admin.display(description="Текст оповещения")
    def notification_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    @admin.display(description="Прочитано?", boolean=True)
    def read_status(self, obj):
        return obj.read


@admin.register(Pet_type)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'breed_count')
    search_fields = ('type_name',)
    actions = [go_to_site]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(breed_total=Count('breed'))

    @admin.display(description="Количество пород", ordering='breed_total')
    def breed_count(self, obj):
        return obj.breed_total


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('breed', 'pet_type_name')
    list_filter = ('pet_type_id',)
    search_fields = ('breed', 'pet_type_id__type_name')
    actions = [go_to_site]

    @admin.display(description="Тип питомца")
    def pet_type_name(self, obj):
        return obj.pet_type_id.type_name if obj.pet_type_id else "—"


@admin.register(Pet_Report)
class PetReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'get_pet_type_name', 'user_name', 'location', 'public_date', 'resolved', 'display_picture')
    list_filter = ('report_type', 'breed_id', 'public_date')
    search_fields = ('description', 'location', 'user_id__first_name', 'title')
    date_hierarchy = 'public_date'
    readonly_fields = ('public_date', 'change_date')
    raw_id_fields = ('user_id', 'breed_id')
    inlines = [FavoriteReportsInline]
    actions = [generate_pdf, go_to_site, delete_selected]

    @admin.display(description="Тип питомца")
    def get_pet_type_name(self, obj):
        if obj.breed_id and hasattr(obj.breed_id, 'pet_type_id'):
            return obj.breed_id.pet_type_id.type_name
        return "—"

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.first_name if obj.user_id else "—"
    
    @admin.display(description="Изображение")
    def display_picture(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.picture.url
            )
        return "Нет изображения"


@admin.register(FavoriteReports)
class FavoriteReportsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'reports_list')
    actions = [go_to_site]

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.get_full_name() or obj.user_id.username if obj.user_id else "—"

    @admin.display(description="Избранные объявления")
    def reports_list(self, obj):
        reports = obj.reports.all()
        if not reports:
            return mark_safe('<i>Нет объявлений</i>')
        
        return format_html_join(
            mark_safe('<br>'),
            '<a href="{}">{}</a>',
            [
                (
                    reverse("admin:animalSearch_pet_report_change", args=[report.pk]),
                    report.title
                )
                for report in reports
            ]
        )
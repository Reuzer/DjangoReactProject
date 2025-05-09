from django.contrib import admin
from django.db.models import Count
from .models import (
    User, Blog, Message, Review, Notification,
    Pet_type, Breed, Pet_Report, FavoriteReports
)
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.urls import reverse


class FavoriteReportsInline(admin.TabularInline):
    model = FavoriteReports.reports.through
    extra = 1
    verbose_name = "Пользователь, добавивший в избранное"
    verbose_name_plural = "Пользователи, добавившие в избранное"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone', 'date_joined', 'password_strength')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'email', 'phone')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined',)

    @admin.display(description="Сложность пароля", ordering="password")
    def password_strength(self, obj):
        return f"{len(obj.password)} символов"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_desc', 'post_date', 'has_picture')
    list_filter = ('post_date',)
    search_fields = ('title', 'short_desc', 'description')
    date_hierarchy = 'post_date'
    readonly_fields = ('post_date',)

    @admin.display(description="Есть изображение?", boolean=True)
    def has_picture(self, obj):
        return bool(obj.picture)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'receiver_name', 'message_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender_id__first_name', 'receiver_id__first_name', 'text')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('sender_id', 'receiver_id')

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

    @admin.display(description="Тип питомца")
    def pet_type_name(self, obj):
        return obj.pet_type_id.type_name if obj.pet_type_id else "—"


@admin.register(Pet_Report)
class PetReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'pet_type_name', 'user_name', 'location', 'public_date', 'resolved')
    list_filter = ('report_type', 'breed_id', 'public_date')
    search_fields = ('description', 'location', 'user_id__first_name', 'title')
    date_hierarchy = 'public_date'
    readonly_fields = ('public_date', 'change_date')
    raw_id_fields = ('user_id', 'breed_id')
    inlines = [FavoriteReportsInline]

    @admin.display(description="Тип питомца")
    def pet_type_name(self, obj):
        return obj.pet_type_id.type_name if obj.pet_type_id else "—"

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.first_name if obj.user_id else "—"


@admin.register(FavoriteReports)
class FavoriteReportsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'reports_list')
    filter_horizontal = ('reports',)

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.first_name if obj.user_id else "—"

    @admin.display(description="Избранные объявления")
    def reports_list(self, obj):
        return format_html_join(
            mark_safe('<br>'),
            '<a href="{}">{}</a>',
            [
                (
                    reverse("admin:animalSearch_pet_report_change", args=[report.pk]),
                    report.title
                )
                for report in obj.reports.all()
            ]
        )

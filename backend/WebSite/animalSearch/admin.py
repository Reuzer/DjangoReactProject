from django.contrib import admin
from django.utils.html import format_html
from .models import (
    User, Blog, Message, Review, Notification,
    Pet_type, Breed, Pet_Report, Report_type, FavoriteReports
) 

class FavoriteReportsInline(admin.TabularInline):
    model = FavoriteReports  # Промежуточная модель ManyToMany
    extra = 5  # Не добавляем пустые формы по умолчанию
    verbose_name = "Пользователь, добавивший в избранное"
    verbose_name_plural = "Пользователи, добавившие в избранное"

    # Добавляем filter_horizontal для удобного выбора пользователей
    filter_horizontal = ('reports',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'registration_date', 'password_strength')
    list_filter = ('registration_date',)
    search_fields = ('name', 'email', 'phone')
    date_hierarchy = 'registration_date'
    list_display_links = ('name', 'email') 
    readonly_fields = ('registration_date',) 

    @admin.display(description="Сложность пароля", ordering="password")
    def password_strength(self, obj):
        return f"{len(obj.password)} символов"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_desc', 'post_date', 'has_picture')
    list_filter = ('post_date',)
    search_fields = ('title', 'short_desc')
    date_hierarchy = 'post_date'
    list_display_links = ('title',)
    readonly_fields = ('post_date',)

    @admin.display(description="Есть изображение?", boolean=True)
    def has_picture(self, obj):
        """Проверяет, есть ли у блога изображение."""
        return bool(obj.picture)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'receiver_name', 'message_preview', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__name', 'receiver__name', 'text')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('sender', 'receiver')

    @admin.display(description="Отправитель")
    def sender_name(self, obj):
        return obj.sender.name if obj.sender else "Неизвестный отправитель"

    @admin.display(description="Получатель")
    def receiver_name(self, obj):
        return obj.receiver.name if obj.receiver else "Неизвестный получатель"

    @admin.display(description="Текст сообщения")
    def message_preview(self, obj):
        """Показывает первые 50 символов текста сообщения."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'rating', 'review_preview', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('user__name', 'text')
    date_hierarchy = 'date'
    readonly_fields = ('date',)

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user.name

    @admin.display(description="Текст отзыва")
    def review_preview(self, obj):
        """Показывает первые 50 символов текста отзыва."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'notification_preview', 'date', 'read_status')
    list_filter = ('read', 'date')
    search_fields = ('user__name', 'text')
    date_hierarchy = 'date'
    readonly_fields = ('date',)

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user.name

    @admin.display(description="Текст оповещения")
    def notification_preview(self, obj):
        """Показывает первые 50 символов текста оповещения."""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    @admin.display(description="Прочитано?", boolean=True)
    def read_status(self, obj):
        return obj.read


@admin.register(Pet_type)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'breed_count')
    search_fields = ('type_name',)

    @admin.display(description="Количество пород")
    def breed_count(self, obj):
        return obj.breed_set.count()


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('breed', 'pet_type_name')
    list_filter = ('pet_type',)
    search_fields = ('breed', 'pet_type__type_name')

    @admin.display(description="Тип питомца")
    def pet_type_name(self, obj):
        return obj.pet_type.type_name


@admin.register(Pet_Report)
class PetReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'pet_type_name', 'user_name', 'location', 'public_date', 'is_found')
    list_filter = ('report_type', 'pet_type', 'public_date')
    search_fields = ('description', 'location', 'user_id__name')
    date_hierarchy = 'public_date'
    readonly_fields = ('public_date', 'change_date')
    raw_id_fields = ('user_id', 'pet_type')
    inline = [FavoriteReportsInline]


    @admin.display(description="Тип питомца")
    def pet_type_name(self, obj):
        return obj.pet_type.type_name if obj.pet_type else "Не указан"

    @admin.display(description="Пользователь")
    def user_name(self, obj):
        return obj.user_id.name if obj.user_id else "Неизвестный пользователь"

    @admin.display(description="Найдено?", boolean=True)
    def is_found(self, obj):
        """Проверяет, является ли отчет о найденном питомце."""
        return obj.report_type == Report_type.FOUND
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
    
@admin.register(FavoriteReports)
class FavoriteReportsAdmin(admin.ModelAdmin):
    list_display = ('user', 'reports_list')
    filter_horizontal = ('reports',)  # Удобный интерфейс для выбора объявлений

    def reports_list(self, obj):
        """Показывает список связанных объявлений."""
        return ", ".join([report.description for report in obj.reports.all()])
    reports_list.short_description = "Избранные объявления"
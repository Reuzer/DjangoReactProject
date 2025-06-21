from rest_framework import permissions

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        # Админ может редактировать любого пользователя кроме superuser
        if obj.is_superuser and not request.user.is_superuser:
            return False
        return request.user.is_admin
    


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, изменение только владельцу или админу
    """
    def has_permission(self, request, view):
        # GET/HEAD/OPTIONS разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для изменений требуется авторизация
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение - только владельцу или админу
        return obj.user_id == request.user or request.user.is_adm
    

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user
from rest_framework import permissions

class IsBuyerOrReadOnly(permissions.BasePermission):
    # 自定義權限只允許對象的所有者編輯它

    def has_object_permission(self, request, view, obj):
        # 讀取權限允許任何請求
        # 總是允許GET, HEAD或OPTIONS請求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 只有訂單的創建者才允許寫權限
        return obj.buyer == request.user
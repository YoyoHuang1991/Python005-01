from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定義權限，只允許對象的所有者編輯它。
    """

    def has_object_permission(self, request, view, obj):
        # 讀取權限允許任何請求
        # 所以我們總是允許Get, Head或Options請求。
        if request.method in permissions.SAFE_METHODS:
            return True

         # 只有該文章的所有者才允許寫權限。
        return obj.owner == request.user
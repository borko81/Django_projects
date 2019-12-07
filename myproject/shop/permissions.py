from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        ''' called only on get when dealing with single resources '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

    def has_permission(self, request, view):
        '''Global permission, doesn't make sense in this permission class'''
        return True

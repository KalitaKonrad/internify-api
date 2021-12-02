from rest_framework import permissions


class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.owner == request.user and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']


class IsCompanyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']

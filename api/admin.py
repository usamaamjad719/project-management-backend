from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_visible']

@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'is_visible']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'text', 'is_visible']


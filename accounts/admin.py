from django.contrib import admin
from .models import DesignRequest, Category

@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'created')
    list_filter = ('status', 'category')
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'new':
            return ('status',)
        return ()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# Register your models here.

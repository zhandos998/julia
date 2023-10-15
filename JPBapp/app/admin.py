from django.contrib import admin

from .models import *
# Register your models here.

class VariableAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    list_display_links = ('name','description')
    search_fields = ('name',)

admin.site.register(Variable, VariableAdmin)
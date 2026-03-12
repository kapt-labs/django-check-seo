from django.contrib import admin

from .models import Keyword, Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("path", "nb_keywords")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "pages_using")

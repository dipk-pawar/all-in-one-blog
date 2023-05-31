from django.contrib import admin
from .models import Category, Blog, About, SocialLink


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "is_featured")
    list_editable = ("is_featured",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Blog, BlogAdmin)

# Register your models here.
admin.site.register(Category)
admin.site.register(About)
admin.site.register(SocialLink)

from django.contrib import admin

from blogs.models import Blog


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ["id", "title", "content"]


admin.site.register(Blog, BlogAdmin)

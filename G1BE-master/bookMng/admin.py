from django.contrib import admin

# Register your models here.
from .models import MainMenu
from .models import Book
from .models import MessageBox
from .models import Comment

admin.site.register(MainMenu)
admin.site.register(Book)



# Adding in a customization of how to view shit
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'web', 'picture', 'price', 'username')
    search_fields = ['name', 'username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'book', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
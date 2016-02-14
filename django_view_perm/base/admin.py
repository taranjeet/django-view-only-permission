from django.contrib import admin

from .models import Book
from .view_only_admin import ViewOnlyAdmin

@admin.register(Book)
class BookAdmin(ViewOnlyAdmin):

    list_display = ('name', 'isbn',)

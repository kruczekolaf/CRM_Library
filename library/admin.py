from django.contrib import admin
from .models import Book, BorrowedBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year', 'copies_available')
    search_fields = ('title', 'author', 'isbn')

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'due_date', 'returned_at', 'is_overdue', 'late_fee')
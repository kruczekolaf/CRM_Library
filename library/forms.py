from django import forms
from .models import Book, BorrowedBook

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = []
from django.contrib import admin
from .models import Book, Loan, Invoice

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Invoice)

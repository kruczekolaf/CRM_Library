from django.db import models
from django.conf import settings
from datetime import timedelta, date


class Book(models.Model):
    isbn = models.CharField(max_length = 20)
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 200)
    published_year = models.IntegerField()
    copies_available = models.IntegerField(default = 1)
    visible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
        
    
    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateField(auto_now_add=True)
    returned_at = models.DateField(null=True, blank=True)

    @property
    def due_date(self):
        return self.borrowed_at + timedelta(days=14)

    @property
    def is_overdue(self):
        return date.today() > self.due_date and not self.returned_at

    @property
    def late_fee(self):
        if self.is_overdue:
            days_late = (date.today() - self.due_date).days
            return days_late * 0.50  # z. B. 0,50 € pro Tag
        return 0
    

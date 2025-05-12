from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-book/', views.add_book, name='add_book'),
    path('return-book/<int:loan_id>/', views.return_book, name='return_book'),
    path('pay-invoice/<int:invoice_id>/', views.pay_invoice, name='pay_invoice'),
    path('datenbank/', views.book_database, name='book_database'),
    path('buch/bearbeiten/<int:book_id>/', views.edit_book, name='edit_book'),
    path('ausleihen/', views.all_loans, name='all_loans'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
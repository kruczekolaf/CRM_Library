from django.urls import path
from . import views
from library.views import startseite
from library.views import bibliothek_suche
from .views import buch_detail


urlpatterns = [
    path('startseite/', views.startseite, name='startseite'),
    path('register/', views.register, name='register'),
    path('buch-hinzufuegen/', views.buch_hinzufuegen, name='buch_hinzufuegen'),
    path('bibliothek/', views.bibliothek, name='bibliothek'),
    path('buch/<int:buch_id>/sichtbarkeit/', views.toggle_visibility, name='toggle_visibility'),
    path('buch/<int:buch_id>/bearbeiten/', views.buch_bearbeiten, name='buch_bearbeiten'),
    path('bibliothek/suche/', bibliothek_suche, name='bibliothek_suche'),
    path('buch/<int:pk>/', buch_detail, name='buch_detail'),
    path('buch/loeschen/<int:book_id>/', views.delete_book, name='delete_book'),
    path('ausleihen/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrowed_id>/', views.return_book, name='return_book'),
]


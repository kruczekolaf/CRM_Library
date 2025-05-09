from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, BorrowBookForm
from library.models import Book, BorrowedBook
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q, Count

@staff_member_required
def buch_hinzufuegen(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Das Buch wurde erfolgreich hinzugefügt.')
            if 'return_dashboard' in request.POST:
                return redirect('dashboard')
            else:
                return redirect('buch_hinzufuegen')  # Standard: Weiter neues Buch
    else:
        form = BookForm()
    return render(request, 'library/buch_hinzufuegen.html', {'form': form})

@staff_member_required
def bibliothek(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'library/bibliothek.html', {'books': books})

@staff_member_required
def toggle_visibility(request, buch_id):
    book = get_object_or_404(Book, id=buch_id)
    if request.method == 'POST':
        book.visible = not book.visible
        book.save()
    return redirect('bibliothek')

@staff_member_required
def buch_bearbeiten(request, buch_id):
    book = get_object_or_404(Book, id=buch_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bibliothek')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/buch_bearbeiten.html', {'form': form, 'book': book})

def startseite(request):
    # Hole die neuesten 8 Bücher, die sichtbar sind und verfügbare Exemplare haben
    newest_books = Book.objects.filter(visible=True, copies_available__gt=0).order_by('-id')[:8]
    
    # Hole die 4 beliebtesten Genres
    genres = Book.objects.filter(visible=True).values('genre').annotate(
        count=Count('genre')).order_by('-count')[:4]
    
    popular_genres = [item['genre'] for item in genres]
    
    # Erstelle ein Dictionary mit Genre-Namen und deren Anzahl an Büchern
    genre_counts = {item['genre']: item['count'] for item in genres}
    
    # Suche nach Büchern, wenn ein Suchbegriff eingegeben wurde
    query = request.GET.get('q')
    search_results = []
    if query:
        search_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        ).filter(visible=True, copies_available__gt=0).order_by('title')
    
    context = {
        'newest_books': newest_books,
        'popular_genres': popular_genres,
        'genre_counts': genre_counts,
        'search_results': search_results,
        'query': query
    }
    
    return render(request, 'startseite.html', context)

def bibliothek_suche(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        ).filter(visible=True, copies_available__gt=0)
    return render(request, 'library/bibliothek_suche.html', {'results': results, 'query': query})

def register(request):
    return render(request, 'register.html')

def buch_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/buch_detail.html', {'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_title = book.title
    book.delete()
    messages.success(request, f'Das Buch "{book_title}" wurde erfolgreich gelöscht.')
    return redirect('bibliothek')


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.copies_available > 0:
        BorrowedBook.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()
        messages.success(request, f"'{book.title}' erfolgreich ausgeliehen.")
    else:
        messages.error(request, f"'{book.title}' ist momentan nicht verfügbar.")

    return redirect('dashboard')

@login_required
def return_book(request, borrowed_id):
    borrowed = get_object_or_404(BorrowedBook, pk=borrowed_id, user=request.user)
    if not borrowed.returned_at:
        borrowed.returned_at = date.today()
        borrowed.save()

        borrowed.book.copies_available += 1
        borrowed.book.save()

        if borrowed.is_overdue:
            messages.warning(request, f"'{borrowed.book.title}' verspätet zurückgegeben. Gebühr: {borrowed.late_fee:.2f} €")
        else:
            messages.success(request, f"'{borrowed.book.title}' erfolgreich zurückgegeben.")

    return redirect('dashboard')
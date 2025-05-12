from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Loan, Invoice
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone

def home(request):
    search_query = request.GET.get('q', '')
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(genre__icontains=search_query) |
            Q(isbn__icontains=search_query) |
            Q(published_year__icontains=search_query),
            visible=True
        )
    else:
        books = Book.objects.none()  # Leeres Queryset, wenn kein Suchbegriff
    top_categories = Book.objects.filter(visible=True).values('genre').annotate(num_loans=Count('loan')).order_by('-num_loans')[:5]
    newest_books = Book.objects.filter(visible=True).order_by('-created_at')[:5]
    context = {
        'books': books,
        'top_categories': top_categories,
        'newest_books': newest_books,
        'search_query': search_query,  # Optional, falls du das Feld im Template vorausfüllen willst
    }
    return render(request, 'library/home.html', context)

@login_required
def dashboard(request):
    my_loans = Loan.objects.filter(user=request.user, is_returned=False)
    my_invoices = Invoice.objects.filter(user=request.user, paid=False)
    return render(request, 'library/dashboard.html', {
        'my_loans': my_loans,
        'my_invoices': my_invoices,
    })

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, visible=True)
    if request.method == 'POST':
        if book.copies_available > 0:
            due = timezone.now() + timezone.timedelta(days=14)
            Loan.objects.create(user=request.user, book=book, due_date=due)
            book.copies_available -= 1
            book.save()
            messages.success(request, 'Buch erfolgreich ausgeliehen!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Keine Exemplare verfügbar.')
    return render(request, 'library/book_detail.html', {'book': book})

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    all_books = Book.objects.all()
    all_loans = Loan.objects.filter(is_returned=False)
    open_invoices = Invoice.objects.filter(paid=False)
    return render(request, 'library/admin_dashboard.html', {
        'all_books': all_books,
        'all_loans': all_loans,
        'open_invoices': open_invoices,
    })

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        isbn = request.POST['isbn']
        title = request.POST['title']
        author = request.POST['author']
        genre = request.POST['genre']
        published_year = request.POST['published_year']
        copies_available = request.POST['copies_available']
        # Korrekte Umwandlung der Checkbox in ein Boolean:
        visible = request.POST.get('visible') == 'on'
        image = request.FILES.get('image')
        Book.objects.create(
            isbn=isbn, title=title, author=author, genre=genre,
            published_year=published_year, copies_available=copies_available,
            visible=visible, image=image
        )
        messages.success(request, 'Buch hinzugefügt!')
        return redirect('admin_dashboard')
    return render(request, 'library/add_book.html')

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user, is_returned=False)
    loan.is_returned = True
    loan.returned_at = timezone.now()
    loan.book.copies_available += 1
    loan.book.save()
    loan.save()

    # 14-Tage-Frist berechnen
    free_period = timedelta(days=14)
    borrowed_for = loan.returned_at - loan.borrowed_at
    if borrowed_for > free_period:
        days_overdue = (borrowed_for - free_period).days
        amount = 1.5 * days_overdue
        Invoice.objects.create(
            user=request.user,
            book=loan.book,
            amount=amount,
            due_date=timezone.now()
        )
    messages.success(request, 'Buch zurückgegeben!')
    return redirect('dashboard')

@login_required
def pay_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user, paid=False)
    if request.method == 'POST':
        invoice.paid = True
        invoice.save()
        messages.success(request, 'Rechnung bezahlt!')
        return redirect('dashboard')
    return render(request, 'library/pay_invoice.html', {'invoice': invoice})

@login_required
@user_passes_test(is_admin)
def book_database(request):
    books = Book.objects.all()
    return render(request, 'library/book_database.html', {'books': books})

@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.genre = request.POST.get('genre', book.genre)
        book.isbn = request.POST.get('isbn', book.isbn)
        book.published_year = request.POST.get('published_year', book.published_year)
        book.copies_available = int(request.POST.get('copies_available', book.copies_available))
        # Für das Checkbox-Feld:
        book.visible = request.POST.get('visible') == 'on'
        book.save()
        messages.success(request, 'Buch erfolgreich bearbeitet!')
        return redirect('book_database')
    return render(request, 'library/edit_book.html', {'book': book})

@login_required
@user_passes_test(is_admin)
def all_loans(request):
    # Alle Ausleihen, sortiert nach Rückgabestatus, neueste zuerst
    loans = Loan.objects.select_related('book', 'user').order_by('-borrowed_at')
    today = timezone.now().date()

    # Zusätzliche Felder berechnen
    for loan in loans:
        # Fälligkeitsdatum als Datum (schon im Model vorhanden)
        loan.due_date_date = loan.due_date.date()
        # Überfälligkeitsberechnung
        if not loan.is_returned and today > loan.due_date_date:
            loan.days_overdue = (today - loan.due_date_date).days
            loan.fee = round(loan.days_overdue * 1.5, 2)
        else:
            loan.days_overdue = 0
            loan.fee = 0
    return render(request, 'library/all_loans.html', {'loans': loans})

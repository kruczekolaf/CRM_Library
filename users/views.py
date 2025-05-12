from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from library.models import BorrowedBook


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registrierung erfolgreich!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form,
        'show_navbar': False,
        'nur_startseite_navbar': True   
    })

@login_required
def ausleihe_view(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user).select_related('book')
    return render(request, 'users/ausleihe.html', {
        'borrowed_books': borrowed_books,
        'show_navbar': True
    })
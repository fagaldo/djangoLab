from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    #  Pobranie pozycji z bazy danych
    news = News.objects.order_by('-create_time')
    # Stworzenie słownika przechowującego elementy bazy danych pod zmienną news
    context = {'news': news}
    # Przesłanie wyrenderowanej strony wraz z dodanymi elementami z bazy danych
    # elementy ze słownika context wykorzytywane są w pliku news/index.html 
    return render(request, 'news/index.html', context)

@login_required(login_url='/login/')
def add(request):
    # Sprawdzenie metody jaką przyszło zapytanie HTTP
    # Jeżeli POST - szukamy danych w ciele zapytania
    # Jeżeli GET - wysyłałym formularz do wypełnienia 
    # (można przesyłać dane w zapytaniu GET - 
    # ale w tym rozwiązaniu tego nie wykorzystujemy)
    if request.method == 'POST':
        
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        # więc tworzymy obiekt formularza z zapytania
        news = NewsForm(request.POST)

        # Jeżeli formularz - czyli dane przesłane z zapytania POST 
        # są proawidłowe dodajemy element do bazy danych 
        if news.is_valid():
            news = news.save(commit=False)
            # news.author = request.user
            news.create_time = timezone.now()
            news.last_edit_time = timezone.now()
            news.save()
            return redirect('view_news')
        # Jeżeli nie są prawidłowe przesyłamy formularz z powrotem do kilenta 
        # Autmatyczny walidator tworzy również pola błędów, które są dostępne po
        # stronie klienta
        else:
            context = {'form': news}
            return render(request, 'news/add.html', context)
    
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        news = NewsForm()
        context = {'form': news}
        return render(request, 'news/add.html', context)
    
@login_required(login_url='/login/')
def edit(request, id):
    news = get_object_or_404(News, id=id)
    if request.method == 'POST':
        
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        # więc tworzymy obiekt formularza z zapytania
        form = NewsForm(request.POST, instance = news)

        # Jeżeli formularz - czyli dane przesłane z zapytania POST 
        # są proawidłowe dodajemy element do bazy danych 
        if form.is_valid():
            form = form.save(commit=False)
            # news.author = request.user
            form.last_edit_time = timezone.now()
            form.save()
            return redirect('view_news')
        # Jeżeli nie są prawidłowe przesyłamy formularz z powrotem do kilenta 
        # Autmatyczny walidator tworzy również pola błędów, które są dostępne po
        # stronie klienta
        else:
            
            context = {{'form': form, 'news': news}}
            return render(request, 'news/edit.html', context)
    
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        form = NewsForm(instance = news)
        return render(request, 'news/edit.html', {'form': form, 'news': news})
@login_required(login_url='/login/')
def delete_news(request, id):
    news = get_object_or_404(News, id=id)
    if request.method == 'POST':
        news.delete()
        return redirect('view_news')  # Zakładając, że masz widok o nazwie 'news_list' dla listy wiadomości
    context = {'news': news}
    return render(request, 'news/delete_news.html', context)
def get(request, id):
    # funkcja get_object_or_404 zwraca element z bazy 
    # danych o danej wartości argumentu
    # lub przesłyła do kilenta błąd
    news = get_object_or_404(News, id=id)
    context = {'news': news}
    return render(request, 'news/view.html', context)
from django.shortcuts import render, redirect
import random, json
from .models import ExamQuestions
from django.core.serializers import serialize

# Create your views here.
def losuj_pytania():
    # Pobierz wszystkie pytania
    wszystkie_pytania = ExamQuestions.objects.all()

    # Przemieszaj pytania
    wylosowane_pytania = random.sample(list(wszystkie_pytania), 3)

    return wylosowane_pytania


def egzamin(request):
    if request.method == 'POST':
        # Pobierz odpowiedzi od użytkownika
        odpowiedzi_uzytkownika = request.POST.getlist('odpowiedz')

        # Pobierz poprawne odpowiedzi
        poprawne_odpowiedzi = request.session.get('odpowiedz', [])

        # Sprawdź, czy odpowiedzi są poprawne i przyznaj punkty
        wynik = sum([1 for odp_uzyt, odp_pop in zip(odpowiedzi_uzytkownika, poprawne_odpowiedzi) if
                     odp_uzyt.lower() == odp_pop.lower()])

        # Zapisz wynik w sesji
        request.session['wynik'] = wynik

        # Przejdz do strony z wynikiem
        return redirect('wynik')
    if 'isstarted' in request.session:
        pass
    else:
        request.session['isstarted'] = 'tak'
        # Jeśli to pierwsze pytanie w quizie, losuj pytania
        wylosowane_pytania = losuj_pytania()
        # Serializacja obiektów do JSON
        pytania_json = serialize('json', wylosowane_pytania)
        pytania = json.loads(pytania_json)

        request.session['pytania'] = [pytanie['fields']['pytanie'] for pytanie in pytania]
        print(request.session['pytania'])
        request.session['odpowiedz'] = [pytanie['fields']['poprawna_odpowiedz'] for pytanie in pytania]

        # Wyświetl wszystkie pytania na jednej stronie
    return render(request, 'exam.html', {'pytania': request.session['pytania']})

def wynik(request):
    del request.session['isstarted']
    procent = request.session['wynik'] / 3 * 100
    context = {
        'wynik': request.session.get('wynik'),
        'proc' : procent
    }
    return render(request, 'end.html', context)
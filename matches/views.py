from django.shortcuts import render, redirect, get_object_or_404
from .models import Match, Klub, Zawodnik, Events
# Create your views here.

def listameczy(request):
    wszystkiemecze = Match.objects.all()
    context = {
        'mecze' : wszystkiemecze,
    }
    return render(request,"meczlist.html",context)

def szczegolymeczu(request, mecz_id):
    mecz = get_object_or_404(Match, pk=mecz_id)
    return render(request, 'szczegolymeczu.html', {'mecz': mecz})
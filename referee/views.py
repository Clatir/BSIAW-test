from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from matches.models import Match, Klub, Zawodnik, Events
from django.db.models import Q
# Create your views here.
from authentication.models import UserProfile, User
from .models import VideoClip
from .forms import EdytujMeczForm, DodajZawodnikaForm, DodajEventForm, DodajMeczForm
from authentication.forms import EdytujUser, EdytujUserPhone
from django.core.mail import EmailMultiAlternatives
import subprocess
import pyodbc
from unidecode import unidecode
from django.conf import settings

def ref_view(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session['username'])
        user_more = UserProfile.objects.get(user = user)
        return render(request, 'referee/referee.html',{'user' : user, 'bonus' : user_more})
    else:
        return redirect('login')

def editusr(requset):
    if 'username' in requset.session:
        user = User.objects.get(username = requset.session['username'])
        if requset.method == 'POST':
            form = EdytujUser(requset.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('referee')
        else:
            form = EdytujUser(instance=user)
        return render(requset, 'userform.html', {'user': user, 'form': form})
    else:
        return redirect('login')

def editusrphon(requset):
    if 'username' in requset.session:
        user = User.objects.get(username = requset.session['username'])
        userph = UserProfile.objects.get(user = user)
        if requset.method == 'POST':
            form = EdytujUserPhone(requset.POST, instance=userph)
            if form.is_valid():
                form.save()
                return redirect('referee')
        else:
            form = EdytujUserPhone(instance=userph)
        return render(requset, 'userformp.html', {'user': user, 'form': form})
    else:
        return redirect('login')

def kol_view(request):
    if 'username' in request.session:
        user = User.objects.get(username=request.session['username'])
        return render(request, 'referee/kolegium.html', {'user': user})
    else:
        return redirect('login')

def spr_view(request):
    if 'username' in request.session:
        return render(request, "referee/sprawozdanie.html")
    else:
        return redirect('login')

def klipy_list(request):
    if 'username' in request.session:
   # Pobierz wszystkich użytkowników z bazy danych
        klipy = VideoClip.objects.all()

    # Przekształć dane do kontekstu szablonu
    #context = {
    #    'klipy': klipy,
    #    'media_url': settings.MEDIA_URL,
    #}
    
        return render(request, "referee/test.html",{"klipy":klipy})
    else:
        return redirect('login')

def listameczy(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session['username'])
        warunek = Q(SedziaG = user) | Q(SedziaA1 = user) | Q(SedziaA2 = user)
        wszystkiemecze = Match.objects.filter(warunek)
        context = {
            'mecze': wszystkiemecze,
        }
        return render(request, "meczlist.html", context)
    else:
        return redirect('login')

def kolmecze(request):
    if 'username' in request.session:
        user = User.objects.get(username = request.session['username'])
        wszystkiemecze = Match.objects.filter(Kolegium = user)
        context = {
            'mecze': wszystkiemecze,
        }
        return render(request, "kolmecze.html", context)
    else:
        return redirect('login')

def szczegolymeczu(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        return render(request, 'szczegolymeczu.html', {'mecz': mecz})
    else:
        return redirect('login')

def szczegolymeczuk(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        return render(request, 'szczegolymeczuk.html', {'mecz': mecz})
    else:
        return redirect('login')


def sprawozdanie(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        if request.method == 'POST':
            form = EdytujMeczForm(request.POST, instance=mecz)
            if form.is_valid():
                form.save()
                return render(request, 'sprawozdanie.html', {'mecz': mecz, 'form': form})
        else:
            form = EdytujMeczForm(instance=mecz)
        return render(request, 'sprawozdanie.html', {'mecz': mecz, 'form': form})
    else:
        return redirect('login')


def sprawozdaniek(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        if request.method == 'POST':
            mecz.status = "zaakceptowane"
            mecz.save()
            return render(request, 'sprawozdaniek.html', {'mecz': mecz, })
        return render(request, 'sprawozdaniek.html', {'mecz': mecz})
    else:
        return redirect('login')


def sgosp(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        gospodarz = mecz.Gosp
        zawodnicy = Zawodnik.objects.filter(klub=gospodarz).order_by('nr')
        return render(request, 'sgosp.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    else:
        return redirect('login')

def sgospk(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        gospodarz = mecz.Gosp
        zawodnicy = Zawodnik.objects.filter(klub=gospodarz).order_by('nr')
        return render(request, 'sgospk.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    else:
        return redirect('login')


def sgosc(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        gosc = mecz.Gosc
        zawodnicy = Zawodnik.objects.filter(klub=gosc).order_by('nr')
        return render(request, 'sgosc.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    else:
        return redirect('login')


def sgosck(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        gosc = mecz.Gosc
        zawodnicy = Zawodnik.objects.filter(klub=gosc).order_by('nr')
        return render(request, 'sgosck.html', {'mecz': mecz, 'zawodnicy': zawodnicy})
    else:
        return redirect('login')

def event(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        wydarzenia = Events.objects.filter(mecz=mecz).order_by('minuta')
        return render(request, 'event.html', {'mecz': mecz, 'wydarzenia': wydarzenia})
    else:
        return redirect('login')

def eventk(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        wydarzenia = Events.objects.filter(mecz=mecz).order_by('minuta')
        return render(request, 'eventk.html', {'mecz': mecz, 'wydarzenia': wydarzenia})
    else:
        return redirect('login')


def addevent(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        if request.method == 'POST':
            form = DodajEventForm(request.POST)
            if form.is_valid():
                form.instance.mecz = mecz
                form.save()
                return redirect('event', mecz.id)
        else:
            form = DodajEventForm
        return render(request, "addevent.html", {'form': form, 'mecz': mecz})
    else:
        return redirect('login')


def addzawodnikh(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        if request.method == 'POST':
            form = DodajZawodnikaForm(request.POST)
            if form.is_valid():
                form.instance.klub = mecz.Gosp
                form.save()
                return redirect('sgosp', mecz.id)
        else:
            form = DodajZawodnikaForm
        return render(request, "addzaw.html", {'form': form, 'mecz': mecz})
    else:
        return redirect('login')


def addzawodnika(request, mecz_id):
    if 'username' in request.session:
        mecz = get_object_or_404(Match, pk=mecz_id)
        if request.method == 'POST':
            form = DodajZawodnikaForm(request.POST)
            if form.is_valid():
                form.instance.klub = mecz.Gosc
                form.save()
                return redirect('sgosc', mecz.id)
        else:
            form = DodajZawodnikaForm
        return render(request, "addzawa.html", {'form': form, 'mecz': mecz})
    else:
        return redirect('login')


def addmecz(request):
    if 'username' in request.session:
        u1 = User.objects.get(username=request.session['username'])
        if request.method == 'POST':
            form = DodajMeczForm(request.POST)
            if form.is_valid():
                form.instance.Kolegium = u1
                mecz = form.save()
                sendinfoSG(mecz)
                sendinfoSA(mecz)
                sendinfoSAa(mecz)
                return redirect("kolmecze")
        else:
            form = DodajMeczForm
        return render(request, "addmecz.html", {'form': form})
    else:
        return redirect('login')


def sendinfoSG(mecz):
    s1 = mecz.SedziaG
    #name = s1.username
    email = s1.email
    plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                    f"Data meczu: {mecz.data}, godzina {mecz.godzina}\n" \
                    f"W: {mecz.miejscowosc}\n" \
                    f"Ul: {mecz.ulica}\n" \
                    f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n"
    message = EmailMultiAlternatives(
        subject="Nowa Obsada",
        body=plain_message,
        from_email=None,
        to=[email],
    )
    try:
        message.send()
    except:
        print("cos nie tak")
    try:
        s2 = UserProfile.objects.get(user = s1)
        phone = s2.phone
        mes = f"Nowa obsada: {mecz.Gosp} - {mecz.Gosc}, Data meczu: {mecz.data}, {mecz.godzina}"
        send_sms_command = f'adb shell service call isms 5 i32 0 s16 "com.android.mms.service" s16 "null" s16 {phone} s16 "null" s16 "\'{mes}\'" s16 "null" s16 "null" i32 0 i64 0'
        subprocess.run(send_sms_command, shell=True)
    except:
        print("cos nie tak")
    #print(f'Nowy mecz {mecz} z sedzia glowny {name} mail {s1.email}')

def sendinfoSA(mecz):
    if mecz.SedziaA1:
        s1 = mecz.SedziaA1
    #name = s1.username
        email = s1.email
        plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                        f"Data meczu: {mecz.data}\n " \
                        f"W: {mecz.miejscowosc}\n" \
                        f"Ul: {mecz.ulica}\n" \
                        f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n"
        message = EmailMultiAlternatives(
            subject="Nowa Obsada",
            body=plain_message,
            from_email=None,
            to=[email],
        )
        try:
            message.send()
        except:
            print("cos nie tak")
        try:
            s2 = UserProfile.objects.get(user=s1)
            phone = s2.phone
            mes = f"Nowa obsada: {mecz.Gosp} - {mecz.Gosc}, Data meczu: {mecz.data}, {mecz.godzina}"
            send_sms_command = f'adb shell service call isms 5 i32 0 s16 "com.android.mms.service" s16 "null" s16 {phone} s16 "null" s16 "\'{mes}\'" s16 "null" s16 "null" i32 0 i64 0'
            subprocess.run(send_sms_command, shell=True)
        except:
            print("cos nie tak")
    #print(f'Nowy mecz {mecz} z sedzia glowny {name} mail {s1.email}')

def sendinfoSAa(mecz):
    if mecz.SedziaA2:
        s1 = mecz.SedziaA2
    #name = s1.username
        email = s1.email
        plain_message = f"Dostales nowa obsade na mecz: {mecz.Gosp} - {mecz.Gosc}\n " \
                        f"Data meczu: {mecz.data}\n " \
                        f"W: {mecz.miejscowosc}\n" \
                        f"Ul: {mecz.ulica}\n" \
                        f"Kolejka: {mecz.kolejka}, {mecz.rozgrywki}\n"
        message = EmailMultiAlternatives(
            subject="Nowa Obsada",
            body=plain_message,
            from_email=None,
            to=[email],
        )
        try:
            message.send()
        except:
            print("cos nie tak")
        try:
            s2 = UserProfile.objects.get(user=s1)
            phone = s2.phone
            mes = f"Nowa obsada: {mecz.Gosp} - {mecz.Gosc}, Data meczu: {mecz.data}, {mecz.godzina}"
            send_sms_command = f'adb shell service call isms 5 i32 0 s16 "com.android.mms.service" s16 "null" s16 {phone} s16 "null" s16 "\'{mes}\'" s16 "null" s16 "null" i32 0 i64 0'
            subprocess.run(send_sms_command, shell=True)
        except:
            print("cos nie tak")
    #print(f'Nowy mecz {mecz} z sedzia glowny {name} mail {s1.email}')
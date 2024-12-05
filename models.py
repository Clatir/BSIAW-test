from django.db import models
from authentication.models import User

# Create your models here.
class Klub(models.Model):
    name = models.CharField(max_length=150)
    liga = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ('przed', 'Przed'),
        ('zlozone', 'Złożone'),
        ('zaakceptowane', 'Zaakceptowane'),
    ]
    RUNDA_CHOICES = [
        ('jesien', 'Jesienna'),
        ('wiosna', 'Wiosenna'),
    ]

    Gosp = models.ForeignKey(Klub, related_name='gospodarz_mecze', on_delete=models.SET_NULL, null=True)
    Gosc = models.ForeignKey(Klub, related_name='gosc_mecze', on_delete=models.SET_NULL, null=True)
    wynik = models.CharField(max_length=8, default='0:0')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='przed')
    data = models.DateField(null=True)
    godzina = models.CharField(max_length=10, null=True)
    ulica = models.CharField(max_length=100, null=True)
    miejscowosc = models.CharField(max_length=100, null=True)
    rozgrywki = models.CharField(max_length=100, null=True)
    runda = models.CharField(max_length=20, choices=RUNDA_CHOICES, null=True)
    kolejka = models.PositiveIntegerField(null=True)
    Kolegium = models.ForeignKey(User, related_name="kolegium_mecz", on_delete=models.SET_NULL, null=True)
    SedziaG = models.ForeignKey(User, related_name="szedziag_meczu", on_delete=models.SET_NULL, null=True)
    SedziaA1 = models.ForeignKey(User, related_name="szedziaa1_meczu", on_delete=models.SET_NULL, null=True, blank=True)
    SedziaA2 = models.ForeignKey(User, related_name="szedziaa2_meczu", on_delete=models.SET_NULL, null=True, blank=True)
    #def name(self):
    #    return f"{self.Gosp} - {self.Gosc}"
    def __str__(self):
        return f"Kolejka: {self.kolejka}  {self.rozgrywki}  {self.Gosp} - {self.Gosc} : {self.data}"

class Zawodnik(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    nr = models.IntegerField()
    klub = models.ForeignKey(Klub, related_name='zawodnicy', on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

class Events(models.Model):
    EVENTS_TYPE =[
        ('zolta_kartka','Zolta_kartka'),
        ('czerwona_kartka', 'Czerwona_kartka'),
        ('gol','Gol'),
    ]
    WHOS = [
        ('gosp','Gospodarz'),
        ('gosc','Gosc'),
    ]
    typ = models.CharField(max_length=50, choices=EVENTS_TYPE)
    minuta = models.IntegerField()
    kto = models.CharField(max_length=50, choices=WHOS)
    nr_zawodnika = models.IntegerField()
    mecz = models.ForeignKey(Match, related_name='wydarzenie_meczowe', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.typ
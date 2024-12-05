from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def home_view(request):


    return render(request, 'group_referee/n.html')
def set_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            User.objects.create_user(username=username, password='unset')
        except:
            messages.error(request, 'Użytkownik już istnieje')
            return HttpResponseRedirect(request.path)
    return render(request, 'group_referee/set_user.html')
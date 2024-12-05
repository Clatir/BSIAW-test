
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import UserProfile
import pyotp
import qrcode
from io import BytesIO

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode

def generate_fernet_key(password: str, salt: bytes = None) -> bytes:
    if not salt:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def generate_qr_code(my_user, password, t_role):
        fa_key = pyotp.random_base32()
        key, salt = generate_fernet_key(password)
        f = Fernet(key)
        b_fa_key = f.encrypt(fa_key.encode())
        try:
            user_profile = UserProfile.objects.get(user=my_user)
            user_profile.fa_key = b_fa_key
            user_profile.salt = salt
            user_profile.save()
        except UserProfile.DoesNotExist:
            if t_role == "unset":
                n_role = "Sedzia"
            else:
                n_role = "Kolegium"
            UserProfile.objects.create(user=my_user, fa_key=b_fa_key, salt=salt, role = n_role)  

        uri = pyotp.totp.TOTP(fa_key).provisioning_uri(name=my_user.username,issuer_name="DZPN")
        qrcode.make(uri)
        qr = qrcode.make(uri)
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)
        qr_base64 = base64.b64encode(qr_io.getvalue()).decode()
        return qr_base64

def validate_pass(password):
    msg = []
    if len(password) < 8:
        msg.append("haslo musi miec co najmiej 8 znakow")
    
    if not any(char.isdigit() for char in password):
        msg.append("Hasło musi zawierać co najmniej jedną cyfrę")

    if not any(char.isupper() for char in password):
        msg.append("Hasło musi zawierać co najmniej jedną dużą literę")

    if not any(char in "!@#$%^&*()_+=" for char in password):
        msg.append("Hasło musi zawierać co najmniej jeden znak specjalny")
    
    return msg


def signup(request):
    if request.method == "POST":
        msg = []
        #user_auth
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if authenticate(request,username = username, password = "ColHaslo1@"):
                msg += validate_pass(password)
                if msg:
                    [messages.error(request,m) for m in msg]
                    return HttpResponseRedirect(request.path)
                user.email = email
                user.set_password(password)
                user.save()
                role = "ColHaslo1@"
                qr = generate_qr_code(user, password,role)
                context = {'qr_code': qr}
                return render(request, 'authentication/signup_done.html',context)
            if authenticate(request,username = username, password = "unset"):
                msg += validate_pass(password)
                if msg:
                    [messages.error(request,m) for m in msg]
                    return HttpResponseRedirect(request.path)
                user.email = email
                user.set_password(password)
                user.save()
                role = "unset"
                qr = generate_qr_code(user, password,role)
                context = {'qr_code': qr}
                return render(request, 'authentication/signup_done.html',context)
            else:
                msg.append('Nieprawidłowa nazwa użytkownika')
                #print("tutaj!")
                #print(user.password)
        except User.DoesNotExist:
            #print("nietutaj!")
            msg.append('Nieprawidłowa nazwa użytkownika')
        msg += validate_pass(password)
        if msg:
            [messages.error(request,m) for m in msg]
            return HttpResponseRedirect(request.path)

    return render(request, 'authentication/signup.html')

def login_view(request):
    if 'username' in request.session:
        return redirect('main_page',request.session['username']) 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        fa_code = request.POST.get('fa_code')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            salt = user_profile.salt
            e_fa_key = user_profile.fa_key
            key,s = generate_fernet_key(password, salt)
            fa_key = Fernet(key).decrypt(e_fa_key).decode()
            
            if not pyotp.TOTP(fa_key).verify(fa_code):
                messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło')
                return render(request, 'authentication/login.html')
            login(request, user)
            request.session['username'] = username
            u1 = User.objects.get(username = username)
            u2 = UserProfile.objects.get(user = u1)
            if u2.role == "Sedzia":
                return redirect('referee')
            if u2.role == "Kolegium":
                return redirect('kolegium')
        
        messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło')
    return render(request, 'authentication/login.html')

def main_page_view(request, username):
    if 'username' in request.session:
        if request.session['username'] == username:
            return render(request, 'authentication/main.html', {'username': username})
        else:
            return redirect('main_page',request.session['username']) 
    else:
        return redirect('login')


def logout_view(request):
    request.session.flush()
    return redirect('login')

# password reset

def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Nieprawidłowy email')
            return render(request, 'authentication/reset_password/reset_password.html')
        
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        context = {'protocol':'http','domain':'localhost:8000','uid': uidb64, 'token': token}
        html_message = render_to_string("authentication/reset_password/password_reset_email.html",context)
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="Resetowanie hasła",
            body=plain_message,
            from_email=None,
            to=[email],
        )
        message.attach_alternative(html_message, "text/html")
        message.send()

        return render(request, 'authentication/reset_password/reset_password_sent.html')
        
    return render(request, 'authentication/reset_password/reset_password.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        messages.error(request, 'Nieprawidłowy link')
        return render(request, 'authentication/reset_password/reset_password.html')

    if not default_token_generator.check_token(user, token):
        messages.error(request, 'Nieprawidłowy link')
        return render(request, 'authentication/reset_password/reset_password.html')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Hasła nie są takie same')
            return render(request, 'authentication/reset_password/password_reset_confirm.html')
        msg = validate_pass(password)
        if msg:
            [messages.error(request,m) for m in msg]
            return render(request, 'authentication/reset_password/password_reset_confirm.html')
        
        user.set_password(password)
        user.save()
        qr = generate_qr_code(user, password)
        context = {'qr_code': qr}
        return render(request, 'authentication/signup_done.html',context)
    
    return render(request, 'authentication/reset_password/password_reset_confirm.html')
def home_view(request):
    return render(request, 'base.html')

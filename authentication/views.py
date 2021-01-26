from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import User
import json
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from validate_email import validate_email


# Account Activation HTML Templated Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.views import View

# Speeding up Django Email Sending using Multithreading
import threading


# Multi-threading
class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.email = msg
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


# Create your views here.
@unauthenticated_user
def userRegistration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # newly created user will automatically be inactive due to receiver from django-signals
            user = form.save()
            usrname = form.cleaned_data.get('username')


            # Send Account activation Code via HTML template Email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain       #  "http://127.0.0.1:8000"
            link = reverse('authenticationApp:activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})    # Inside the token_generator of "utils.py", encoded the "user.is_active=Ture"
            # the "reverse('authenticationApp:activate'....." came from the name of the "urls.py".

            activate_url = 'http://'+domain+link

            email_subject = 'Activate you account'
            from_email = 'python4dia@gmail.com'
            to_email = user.email

            Context = { 'username': user.username, 'activate_url':activate_url, }

            text_content = render_to_string('authentication/email_template/account_activation.txt', Context)
            html_content = render_to_string('authentication/email_template/account_activation.html', Context)

            msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            # msg.send()
            EmailThread(msg).start()    # sends email fast


            messages.success(
                request, 
                'An account is created for "%s" \nPlease check your email for activation' % (usrname)
            )
            # messages.success(request, 'You are logged in as %s!' % (usrname))
            # messages.success(request, 'New User Created: %s!' % (usrname))

            return redirect('expensesApp:home')
    
    context = {
        'title':'Registration',
        'form':form,
    }
    return render(request, 'authentication/register.html', context)


# Redirected link to the login page after account activation
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # check_token: Check that an account activation token is correct for a given user. Simply checks if the token is already been used or not
            if not token_generator.check_token(user, token):
                messages.warning(request, 'Your account is already activated.')
                return redirect('authenticationApp:login')

            if user.is_active:
                return redirect('authenticationApp:login')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                return redirect('authenticationApp:login')
        except Exception as ex:
            pass

# Real-time username validation checker while registering
@method_decorator(csrf_exempt)
def usernameValidation(request):
    if request.method == "POST":
        data = json.loads(request.body)                     # 'request.body' is a byte string, though json accepts both byte-string & unicode string, so the ".decode('UTF-8')" is not necessary.
        # return JsonResponse(data)                         # displays all the key:value pairs of the json object (in this case, "request.body") for testing purpose.
        username = data['username']   
        # return HttpResponse(username)                     # displays the username value as an http-response
        # return JsonResponse({'username':username})        # displays the inserted 'username' value for testing purpose

        # Check if username contains alpha-numeric character
        if not str(username).isalnum():
            return JsonResponse({
                'username_error':'Username should only contain alpha-numeric characters!',
            }, status=400)
        # Check if the username is already taken
        username_exist = User.objects.filter(username=username)
        if username_exist.exists():
            return JsonResponse({
                'username_error':'Username is not available!',
            }, status=409)
        
        return JsonResponse({
            'username_valid':True,
        })

# Real-time email validation checker while registering
@method_decorator(csrf_exempt)
def emailValidation(request):
    if request.method == "POST":
        data = json.loads(request.body)                 # 'request.body' is a byte string, though json accepts both byte-string & unicode string, so the ".decode('UTF-8')" is not necessary.
        # return JsonResponse(data)                     # displays all the key:value pairs of the json object (in this case, "request.body") for testing purpose.
        email = data['email']
        # return HttpResponse(email)                    # displays the inserted email value as an http-response for testing purpose
        # return JsonResponse({'email':email})          # displays the inserted 'email' value for testing purpose

        # Check if it's a valid email format
        if not validate_email(email):
            return JsonResponse({
                'email_error':'Email address is invalid!',
            }, status=400)
        # Check if the email is already taken
        email_exist = User.objects.filter(email=email)
        if email_exist.exists():
            return JsonResponse({
                'email_error':'Email is already taken!',
            }, status=409)
        
        return JsonResponse({
            'email_valid':True,
        })




@unauthenticated_user
def userLogin(request):
    form = LoginUserForm()
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            usrName = form.cleaned_data.get('username')
            passwrd = form.cleaned_data.get('password')
            user = authenticate(request, username=usrName, password=passwrd)
            if user is not None:
                login(request, user)
                messages.info(request, 'Logged in as %s' % (usrName))
                return redirect('expensesApp:home')
            else:
                # print('Username/password is invalid!')
                # messages.info(request, 'Username/password is incorrect')
                return redirect('authenticationApp:login')

    context = {
        'title':'Login',
        'form':form,
    }
    return render(request, 'authentication/login.html', context)



def userLogout(request):
    logout(request)
    messages.info(request, 'You are logged out!')
    return redirect('authenticationApp:login')
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



# Create your views here.
@unauthenticated_user
def userRegistration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            usrname = form.cleaned_data.get('username')
            # messages.success(
            #     request, 
            #     'An account is created for "%s" \nPlease check your email for activation' % (usrname)
            # )
            # messages.success(request, 'You are logged in as %s!' % (usrname))
            messages.success(request, 'New User Created: %s!' % (usrname))

            return redirect('expensesApp:home')
    
    context = {
        'title':'Registration',
        'form':form,
    }
    return render(request, 'authentication/register.html', context)

# Real-time username validation checker
@method_decorator(csrf_exempt)
def usernameValidation(request):
    if request.method == "POST":
        data = json.loads(request.body)                 # 'request.body' is a byte string, though json accepts both byte-string & unicode string, so the ".decode('UTF-8')" is not necessary.
        # return JsonResponse(data)                     # displays all the key:value pairs of the json object (in this case, "request.body") for testing purpose.
        username = data['username']   
        # return HttpResponse(username)                      # displays the username value as an http-response
        # return JsonResponse({'username':username})    # displays the inserted 'username' value for testing purpose

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

# Real-time email validation checker
@method_decorator(csrf_exempt)
def emailValidation(request):
    if request.method == "POST":
        data = json.loads(request.body)                 # 'request.body' is a byte string, though json accepts both byte-string & unicode string, so the ".decode('UTF-8')" is not necessary.
        # return JsonResponse(data)                     # displays all the key:value pairs of the json object (in this case, "request.body") for testing purpose.
        email = data['email']
        # return HttpResponse(email)                      # displays the email value as an http-response
        # return JsonResponse({'email':email})    # displays the inserted 'email' value for testing purpose

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
            if user is None:
                messages.error(request, 'Invalid username/password')
                return redirect('authenticationApp:login')
            else:
                login(request, user)
                messages.info(request, 'Logged in as %s' % (usrName))
                return redirect('expensesApp:home')

    context = {
        'title':'Login',
        'form':form,
    }
    return render(request, 'authentication/login.html', context)



def userLogout(request):
    logout(request)
    messages.info(request, 'You are logged out!')
    return redirect('authenticationApp:login')
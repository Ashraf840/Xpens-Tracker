from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user


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
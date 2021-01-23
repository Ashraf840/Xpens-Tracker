from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='authenticationApp:login')
def index(request):
    context = {
        'title':"Dashboard",
    }
    return render(request, 'expensesapp/index.html', context)


@login_required(login_url='authenticationApp:login')
def addExpense(request):
    context = {
        'title':"Add Expense",
    }
    return render(request, 'expensesapp/addExpense.html', context)
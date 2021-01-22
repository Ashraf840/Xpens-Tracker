from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title':"Dashboard",
    }
    return render(request, 'expensesapp/index.html', context)


def addExpense(request):
    context = {
        'title':"Add Expense",
    }
    return render(request, 'expensesapp/addExpense.html', context)
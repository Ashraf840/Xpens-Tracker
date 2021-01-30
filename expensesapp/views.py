from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url='authenticationApp:login')
def index(request):
    context = {
        'title':"Dashboard",
    }
    return render(request, 'expensesapp/index.html', context)


@login_required(login_url='authenticationApp:login')
def expenseList(request):
    expenselist = Expense.objects.filter(owner=request.user)
    user = request.user
    z = [ 1, 2, 3, 4, 5]
    # z = 0
    # x = 1
    # import pdb
    # pdb.set_trace()
    context = {
        'title':"Expense List",
        'expenseList':expenselist,
        'user':user,
        'z':z,
        # 'x':x,
    }
    return render(request, 'expensesapp/expenseList.html', context)


@login_required(login_url='authenticationApp:login')
def addExpense(request):
    user = request.user
    categories = Category.objects.filter(categorytype='Expense', owner=user)
    context = {
        'title':"Add Expense",
        'categories':categories,
        'values':request.POST,
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        expenseDate = request.POST['expenseDate']
        user = request.user

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expensesapp/createExpense.html', context)
        else:
            # create category row for the particular user 
            Expense.objects.create(amount=amount, date=expenseDate, description=description, owner=user, category=category)
            messages.info(request, 'New expense added successfully')
            return redirect('expensesApp:createNewExpense')


    return render(request, 'expensesapp/createExpense.html', context)
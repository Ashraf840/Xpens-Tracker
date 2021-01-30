from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

# This is the MAIN DASHBOARD
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

    context = {
        'title':"Expense List",
        'expenseList':expenselist,
        'user':user,
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
            Expense.objects.create(amount=amount, date=expenseDate, description=description, owner=user, category=category)
            messages.info(request, 'New expense added successfully')
            return redirect('expensesApp:createNewExpense')


    return render(request, 'expensesapp/createExpense.html', context)


@login_required(login_url='authenticationApp:login')
def categoryList(request):
    user = request.user
    categoryList_income = Category.objects.filter(owner=request.user, categorytype='Income')
    categoryList_expense = Category.objects.filter(owner=request.user, categorytype='Expense')
    context = {
        'title':"Category List",
        'user':user,
        'categoryList_income':categoryList_income,
        'categoryList_expense':categoryList_expense,
    }
    return render(request, 'expensesapp/categoryList.html', context)


@login_required(login_url='authenticationApp:login')
def addCategory(request):
    cate_types = {
        'Income':'Income',
        'Expense':'Expense',
    }

    context = {
        'title':"Add Category",
        'cate_types':cate_types,
    }

    if request.method == 'POST':
        CateName = request.POST['cateName']
        CateType = request.POST['cateType']

        if not CateName:
            messages.error(request, 'Category name is required')
            return render(request, 'expensesapp/createCategory.html', context)
        else:
            user = request.user
            Category.objects.create(name=CateName, owner=user, categorytype=CateType)
            messages.info(request, 'New category added successfully')
            return redirect('expensesApp:createNewCategory')
        # import pdb
        # pdb.set_trace()

    
    return render(request, 'expensesapp/createCategory.html', context)
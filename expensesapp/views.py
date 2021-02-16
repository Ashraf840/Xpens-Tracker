from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.utils.timezone import now
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Q      # for making complex search queries
from userpreferences.models import UserPreference
import pdb



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
    expenselist = Expense.objects.filter(owner=request.user).order_by('-id')
    user = request.user

    # Fetch & store the currency preferences set by the particular user. Put inside try/except as some user might go to the expense-list page before selecting the preferred currency.
    try:
        currencyPref = UserPreference.objects.get(user=user).currency
    except UserPreference.DoesNotExist:
        currencyPref = 'Not Selected'

    # Pagination
    expenselistPagination = expenselist
    paginator = Paginator(expenselistPagination, 5)
    page = request.GET.get('page')
    expenselist = paginator.get_page(page)

    context = {
        'title':"Expense List",
        'expenseList':expenselist,
        'user':user,
        'currencyPref':currencyPref,
    }
    return render(request, 'expensesapp/expenseList.html', context)


@login_required(login_url='authenticationApp:login')
def addExpense(request):
    user = request.user
    categories = Category.objects.filter(categorytype='Expense', owner=user)

    # This context is placed at the beginning, because the specified 'categories' are passed to the template.
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
        # user = request.user

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expensesapp/createExpense.html', context)
        
        if not expenseDate:
            messages.error(request, 'Expense date is required')
            return render(request, 'expensesapp/createExpense.html', context)

        Expense.objects.create(amount=amount, date=expenseDate, description=description, owner=user, category=category)
        messages.info(request, 'New expense added successfully')
        return redirect('expensesApp:createNewExpense')


    return render(request, 'expensesapp/createExpense.html', context)


def search_expenses(request):
    if request.method == 'POST':
        user = request.user
        
        # the 'searchText' is gotten from the (body: JSON.stringify({ 'searchText':searchValue, }),) of the fetch method of the usernameInput's eventListener inside the 'searchExpense.js'
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter( 
            Q(amount__istartswith=search_str, owner=user) | 
            Q(date__istartswith=search_str, owner=user) | 
            Q(description__icontains=search_str, owner=user) | 
            Q(category__istartswith=search_str, owner=user) 
            )

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='authenticationApp:login')
def updateExpense(request, id):
    user = request.user
    categories = Category.objects.filter(categorytype='Expense', owner=user)
    expenseItem = Expense.objects.get(pk=id)

    dateFormat = "%Y-%m-%d"
    expenseItemDateFomated = expenseItem.date.strftime(dateFormat)

    context = {
        'title':"Update Expense",
        'categories':categories,
        'expenseItem':expenseItem,
        'expenseItemDateFomated':expenseItemDateFomated,
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        expenseDate = request.POST['expenseDate']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expensesapp/editExpense.html/', context)    # don't need to add 'id' in the URL, the context is getting populated using 'amount', 'category', 'description', 'expenseDate' from the variables after POST req.
        else:
            # push update every objects of the 'Expense' django-model  (items)
            expenseItem.amount = amount
            expenseItem.date = expenseDate
            expenseItem.description = description
            expenseItem.owner = user
            expenseItem.category = category

            expenseItem.save()

            # messages.info(request, 'Expense updated successfully: %s---%s---%s---%s---%s---Expense_ID: %s' % (amount, category, description, expenseDate, user, id))
            # messages.info(request, 'Expense updated successfully: %s---%s---%s---%s---%s---Expense_ID: %s' % (amount, category, description, expenseDate, user, expenseItem.id))
            messages.info(request, 'Expense updated successfully')
            return redirect('expensesApp:addExpense')   # redirect to expense-list

    return render(request, 'expensesapp/editExpense.html', context)



@login_required(login_url='authenticationApp:login')
def deleteExpense(request, id):
    expenseData = Expense.objects.get(pk=id)
    expenseData.delete()

    messages.info(request, 'Expense data deleted successfully: %s' % (expenseData.category))
    return redirect('expensesApp:addExpense')



@login_required(login_url='authenticationApp:login')
def categoryList(request):
    user = request.user
    # pdb.set_trace()
    categoryList_income = Category.objects.filter(owner=request.user, categorytype='Income').order_by('-id')
    categoryList_expense = Category.objects.filter(owner=request.user, categorytype='Expense').order_by('-id')

    # Category: Income (Paginator)
    categoryList_incomePagination = categoryList_income
    paginatorIncomeCate = Paginator(categoryList_incomePagination, 5)
    pageIncomeCate = request.GET.get('page')
    categoryList_income = paginatorIncomeCate.get_page(pageIncomeCate)
    
    # Category: Expense (Paginator)
    categoryList_expensePagination = categoryList_expense
    paginatorExpenseCate = Paginator(categoryList_expensePagination, 5)
    pageExpenseCate = request.GET.get('page')
    categoryList_expense = paginatorExpenseCate.get_page(pageExpenseCate)

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
    
    return render(request, 'expensesapp/createCategory.html', context)



@login_required(login_url='authenticationApp:login')
def updateCategory(request, id):
    user = request.user
    category = Category.objects.get(pk=id)
    cate_types = {
        'Income':'Income',
        'Expense':'Expense',
    }

    context = {
        'title':"Update Category",
        'category':category,
        'cate_types':cate_types,
    }

    if request.method == 'POST':
        cateName = request.POST['cateName']
        cateType = request.POST['cateType']

        if not cateName:
            messages.error(request, 'Category name is required')
            return render(request, 'expensesapp/editCategory.html/', context)    # don't need to add 'id' in the URL, the context is getting populated using 'cateName', 'cateType' from the variables after POST req.
        else:
            # push update every objects of the 'Category' django-model  (items)
            category.name = cateName
            category.categorytype = cateType

            category.save()

            messages.info(request, 'Category updated successfully')
            return redirect('expensesApp:categorylist')   # redirect to category-list

    return render(request, 'expensesapp/editCategory.html', context)


@login_required(login_url='authenticationApp:login')
def deleteCategory(request, id):
    categoryData = Category.objects.get(pk=id)
    categoryData.delete()

    messages.info(request, 'Expense deleted successfully: %s' % (categoryData.name))
    return redirect('expensesApp:categorylist')
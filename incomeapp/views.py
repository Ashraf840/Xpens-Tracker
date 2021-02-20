from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income
from expensesapp.models import Category
from userpreferences.models import UserPreference
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Q      # for making complex search queries
from django.contrib import messages
import pdb




# Create your views here.
@login_required(login_url='authenticationApp:login')
def incomeList(request):
    user = request.user
    incomeList = Income.objects.filter(owner=user).order_by('-id')

    # Fetch & store the currency preferences set by the particular user. Put inside try/except as some user might go to the expense-list page before selecting the preferred currency.
    try:
        currencyPref = UserPreference.objects.get(user=user).currency
    except UserPreference.DoesNotExist:
        currencyPref = 'Not Selected'


    # Pagination
    incomelistPagination = incomeList
    paginator = Paginator(incomelistPagination, 5)
    page = request.GET.get('page')
    incomeList = paginator.get_page(page)

    context = {
        'title':"Income List",
        'incomeList':incomeList,
        'currencyPref':currencyPref,
    }
    return render(request, 'incomeapp/incomeList.html', context)


def search_income(request):
    if request.method == 'POST':
        user = request.user
        
        # the 'searchText' is gotten from the (body: JSON.stringify({ 'searchText':searchValue, }),) of the fetch method of the usernameInput's eventListener inside the 'searchIncome.js'
        search_str = json.loads(request.body).get('searchText')

        income = Income.objects.filter( 
            Q(amount__istartswith=search_str, owner=user) | 
            Q(date__istartswith=search_str, owner=user) | 
            Q(description__icontains=search_str, owner=user) | 
            Q(category__istartswith=search_str, owner=user) 
            )

        data = income.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='authenticationApp:login')
def addIncome(request):
    user = request.user
    categories = Category.objects.filter(categorytype='Income', owner=user)
    
    # This context is placed at the beginning, because the specified 'categories' are passed to the template.
    context = {
        'title':"Add Income",
        'categories':categories,
        'values':request.POST,
    }

    if request.method == 'POST':
        # req_post = request.POST
        # pdb.set_trace()
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        incomeDate = request.POST['incomeDate']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomeapp/createIncome.html', context)

        if not incomeDate:
            messages.error(request, 'Income date is required')
            return render(request, 'incomeapp/createIncome.html', context)

        Income.objects.create(amount=amount, date=incomeDate, description=description, owner=user, category=category)
        messages.info(request, 'New expense added successfully')

    return render(request, 'incomeapp/createIncome.html', context)


@login_required(login_url='authenticationApp:login')
def updateIncome(request, id):
    user = request.user
    categories = Category.objects.filter(categorytype='Income', owner=user)
    incomeItem = Income.objects.get(pk=id)

    dateFormat = "%Y-%m-%d"
    incomeItemDateFomated = incomeItem.date.strftime(dateFormat)

    context = {
        'title':"Update Income",
        'categories':categories,
        'incomeItem':incomeItem,
        'incomeItemDateFomated':incomeItemDateFomated,
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        incomeDate = request.POST['incomeDate']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'incomeapp/editIncome.html', context)    # don't need to add 'id' in the URL, the context is getting populated using 'amount', 'category', 'description', 'expenseDate' from the variables after POST req.
        else:
            # push update every objects of the 'Income' django-model  (items)
            incomeItem.amount = amount
            incomeItem.date = incomeDate
            incomeItem.description = description
            incomeItem.owner = user
            incomeItem.category = category

            incomeItem.save()

            # messages.info(request, 'Income updated successfully: %s---%s---%s---%s---%s---Income_ID: %s' % (amount, category, description, IncomeDate, user, id))
            # messages.info(request, 'Income updated successfully: %s---%s---%s---%s---%s---Income_ID: %s' % (amount, category, description, IncomeDate, user, IncomeItem.id))
            messages.info(request, 'Income updated successfully')
            return redirect('incomeApp:incomeList')   # redirect to Income-list

    return render(request, 'incomeapp/editIncome.html', context)


@login_required(login_url='authenticationApp:login')
def deleteIncome(request, id):
    incomeData = Income.objects.get(pk=id)
    incomeData.delete()

    messages.info(request, 'Income data deleted successfully: %s' % (incomeData.category))
    return redirect('incomeApp:incomeList')
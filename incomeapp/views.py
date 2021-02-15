from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Income
from userpreferences.models import UserPreference
from django.core.paginator import Paginator




# Create your views here.
@login_required(login_url='authenticationApp:login')
def incomeList(request):
    user = request.user
    incomeList = Income.objects.filter(owner=user)

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
from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages


# Create your views here.
def index(request):
    currency_list = []

    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')      # just the file path

    # used to read the ".json" file (path) using the mode 'r', means 'read'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)     # convert & assign that json file into a python dictionary variable

        # assign all the objects/dict items into a python list
        for k,v in data.items():
            currency_list.append({'name':k, 'value':v})

        # add python debugger to test the 'file_path' & 'currency_list'
        # import pdb
        # pdb.set_trace()


    # check if any row regarding this user exists in the 'UserPreference' model
    u_pref_exitsts = UserPreference.objects.filter(user=request.user).exists()
    # if the UserPreference doesn't have any user row initially, first set the user_preferences to None
    user_preferences = None
    # otherwise if it has, then grab the same user (logged-in) from the similar user from the UserPreference model
    if u_pref_exitsts:
        user_preferences = UserPreference.objects.get(user=request.user)


    if request.method == "POST":
        currency = request.POST['currency']
        # if the UserPreference does exist, then save it
        if u_pref_exitsts:
            user_preferences.currency = currency
            user_preferences.save()
        # if not, then create a new table-row regarding this UserPreference
        else:
            currency = request.POST['currency']
            UserPreference.objects.create(user=request.user, currency=currency)
        
        messages.info(request, 'Changes Saved!')
    
       
    context = {
        'title':'Settings',
        'currencies':currency_list,
        'user_preferences':user_preferences,
    }  
    return render(request, 'userpreferences/index.html', context)



    
    
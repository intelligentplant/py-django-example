from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

import intelligent_plant.app_store_client as app_store

# Create your views here.
def index(request):
    # check if the user has an access token stored in their session
    # if they do they are logged in otherwise send them the the login page
    if 'access_token' in request.session:
        return HttpResponse(request.app_store_client.get_user_info()['UserId'])
    else:
        return HttpResponseRedirect('/auth/login')
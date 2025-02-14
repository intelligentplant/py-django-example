from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

import intelligent_plant.app_store_client as app_store

# Create your views here.
def index(request):
    # check if the user has an access token stored in their session
    # if they do they are logged in otherwise send them the the login page
    if 'access_token' in request.session:
        data_sources = request.data_core_client.get_data_sources()
        context = {
            "data_sources": data_sources,
        }
        return render(request, "tag_browser/index.html", context)
    else:
        return HttpResponseRedirect('/auth/login')
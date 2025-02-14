from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.conf import settings

import pkce

import intelligent_plant.app_store_client as app_store

import auth.client_handler as client_handler

APP_ID = getattr(settings, "APP_ID", None)
APP_SECRET = getattr(settings, "APP_SECRET", None)
REDIRECT_URL = getattr(settings, "REDIRECT_URL", None)

def login(request):
    # generate a pkce code challenge
    code_verifier, code_challenge = pkce.generate_pkce_pair()

    # store the code verifier in the session so that we can use it later
    request.session['code_verifier'] = code_verifier

    # generate the o auth login url, this will send the user to the consent screen
    consent_screen_url = app_store.get_authorization_code_grant_flow_url(APP_ID, REDIRECT_URL, ['UserInfo', 'DataRead'], code_challenge=code_challenge, code_challenge_method='S256')

    # redirect the user to the consent screen
    return HttpResponseRedirect(consent_screen_url)


def logout(request):
    client_handler.logout(request)
    return HttpResponse("You're logged out.")

def oauth_callback(request):
    # retireve the code verifier from the user's session
    code_verifier = request.session['code_verifier']

    # get the auth code from the query string parameters, this was issued by the app store
    auth_code = request.GET['code']

    # echange the auth code with the app store for an access token
    app_store_client = app_store.complete_authorization_code_grant_flow(auth_code, APP_ID, APP_SECRET, REDIRECT_URL, code_verifier=code_verifier)

    # delete the code verifier from the session, we don't need it anymore
    del request.session['code_verifier']

    user_info = app_store_client.get_user_info()

    # store the app store client's authorization information to the user's session
    request.session["user_info"] = user_info
    request.session["access_token"] = app_store_client.access_token
    request.session["expiry_time"] = app_store_client.expiry_time
    request.session["refresh_token"] = app_store_client.refresh_token

    return HttpResponseRedirect('/')
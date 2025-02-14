import time

import intelligent_plant.app_store_client as app_store



def logout(request):
     # delete the session information we stored during login
    try:
        del request.session["access_token"]
    except KeyError:
        pass
    try:
        del request.session["refresh_token"]
    except KeyError:
        pass

    try:
        del request.session["expiry_time"]
    except KeyError:
        pass

    try:
        del request.session["use_info"]
    except KeyError:
        pass




def client_middleware(get_response):
    # One-time configuration and initialization.

    # run the next request
    def next(request):
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'access_token' in request.session:
            access_token = request.session['access_token']

            expiry_time = request.session['expiry_time'] if 'expiry_time' in request.session else None
            refresh_token = request.session['refresh_token'] if 'refresh_token' in request.session else None

            request.app_store_client = app_store.AppStoreClient(access_token, refresh_token)
            request.app_store_client.expiry_time = expiry_time

            # check for session expiry
            if time.time() > expiry_time:
                try:
                    # attempt to refresh the session
                    request.app_store_client = request.app_store_client.refresh_session()
                    request.session['access_token'] = request.app_store_client.access_token
                    request.session['refresh_token'] = request.app_store_client.refresh_token
                    request.session['expiry_time'] = request.app_store_client.expiry_time
                except:
                    # an error occurred, log out
                    logout(request)
                    return next(request)

            # if the time is still greater than the expiry time we need to log out
            if time.time() > request.app_store_client.expiry_time:
                logout(request)
                return next(request)

            # finally instantiate a data core client from the app store client
            request.data_core_client = request.app_store_client.get_data_core_client()

        return next(request)

    return middleware
# Intelligent Plant Django Web App Example

This is a minimal web app showing how to query the industrial app store data API using Django.

## Setting Up

Install the necessary requirements using (we recommend using a virtual environment):

```bash
pip install -r requirements.txt
```

In order for this example to run correctly you must register as a developer with the Industrial App Store: [https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers](https://wiki.intelligentplant.com/doku.php?id=dev:app_store_developers)

You must then create an app registration to get an app ID and app secret. Register `http://localhost:8080/auth/oauth_callback` as a redirect URL for your app.

Create a file in the route of this repository called `.env` with the following content:

```
APP_ID=<your app id>
APP_SECRET=<your app secret>
REDIRECT_URL=http://localhost:8080/auth/oauth_callback
```

Generate and apply migartions:

```bash
python manage.py makemigrations
python manage.py migrate
```

You can now run the web server using (this must be on port 8080 for the redirect URL to be correct):

```bash
python manage.py runserver 8080
```

Open your browser to [http://localhost:8080](http://localhost:8080). You will be prompted to log in to the app store. Once you have logged in you will be shown a list of the data sources you authorised to demonstrate that we can no query the Industrial App Store data API.

## Code Overview

The `auth` module is where the authroization code flow is implemented. This is an implemenation of the authorization grant flow with PKCE extension. You can try this out yourself in the [OAuth Playground](https://www.oauth.com/playground/index.html).

The `auth` module defines 3 URLs:
 * `/auth/login` which redirects the user to the Industrial App Store consent screen. 
 * `/auth/oauth_callback` this is where the Industrial App Store redirects the user to once they have logged in. This endpoint exchanges the authorization code with the Industrial App Store to get an access token.
 * `/auth/logout` this deletes all information that we have stored in the user's session.

 The `auth` module also provides middleware which takes the access token stored in the user's session and re-instantiates the app store and data core client objects. This allows other views to more easily use the data API as demonstrated in the `tag_browser` index view, which does not have to concern itself with authentication details, it just uses the provided data core client object.

### Login Flow

1. When the user navigates to [http://localhost:8080](http://localhost:8080) the `tag_browser.views.index(..)` function is executed.
1. `tag_browser.views.index(..)` checks if the user's session contains an access token, if it does the user is logged in, otherwise the user needs to be logged in and is recirected to `/auth/login`
1. The request to `/auth/login` is handled by `auth.views.login(..)`. This function generates a code challenge verifier pair fo PKCE and generates URL for the consent screen based on the app configuration in `django_example/settings.py`.
1. The user is redirected to the consent screen where they can select data sources to authorise. The consent screen redirects them back to the redirect URL (which must be registered with the app registration).
1. Once redirect back from the consent screen `/auth/oauth_callback` causes `auth.views.oauth_callback(..)` to be called, this exchanges the authorization code prodived by the Industrial app store for an access token (which is automatically converted into an `AppStoreClient` object by the `intelligent_plant` module).
1. The user's app store profile information, access token, refresh token (if there is one), and expiry time are saved to the user's session and the user is recirected back to `/`.
1. The `auth.client_handler` middleware runs for each request and if a non-expired access token is available it converts that token into an app store client and data core client. If the token has expired it attempts to refresh it. This middleware will also log the user out if their session can't be refreshed.
1. `tag_browser.views.index(..)` now has a valid access token so it can access the data core client object created by the `auth.client_handler` middleware. It uses this to request the authorized data sources.

In a procution application you may want to make a few changes to this flow:
1. When the user's session cannot be refreshed you could redirect them to the login flow instead of logging them out.
1. You may want to use the OAuth flows `state` variable or the user's session to preserve application information (such as which page the user is trying to open) throughout the login flow.
1. You could have middleware redirect the user to the start of the flow if they aren't logged in so that each page doesn't have to check itself.

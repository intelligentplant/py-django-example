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
APP_ID=<you app id>
APP_SECRET=<you app secret>
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
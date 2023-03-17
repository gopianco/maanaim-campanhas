# Django running on Vercel


## Tutorial


### Install Django

```
$ mkdir vercel-django-core
$ cd vercel-django-core
$ pip install Django
$ django-admin startproject maanaim_campanhas .
```

### Add an app

```
$ python manage.py startapp core
```

Add the new app to your application settings (`maanaim_campanhas/settings.py`):
```python
# maanaim_campanhas/settings.py
INSTALLED_APPS = [
    # ...
    'core',
]
```

Be sure to also include your new app URLs in your project URLs file (`maanaim_campanhas/urls.py`):
```python
# maanaim_campanhas/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('core.urls')),
]
```


#### Create the first view

Add the code below (a simple view that returns the current time) to `core/views.py`:
```python
# core/views.py
from datetime import datetime

from django.http import HttpResponse


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)
```


#### Add the first URL

Add the code below to a new file `core/urls.py`:
```python
# core/urls.py
from django.urls import path

from core.views import index


urlpatterns = [
    path('', index),
]
```


### Test your progress

Start a test server and navigate to `localhost:8000`, you should see the index view you just
created:
```
$ python manage.py runserver
```

### Get ready for Now

#### Add the Now configuration file

Create a new file `vercel.json` and add the code below to it:
```json
{
    "builds": [{
        "src": "maanaim_campanhas/wsgi.py",
        "use": "@ardnt/vercel-python-wsgi",
        "config": { "maxLambdaSize": "15mb" }
    }],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "maanaim_campanhas/wsgi.py"
        }
    ]
}
```
This configuration sets up a few things:
1. `"src": "maanaim_campanhas/wsgi.py"` tells Vercel that `wsgi.py` contains a WSGI application
2. `"use": "@ardnt/vercel-python-wsgi"` tells Now to use the `vercel-python-wsgi` builder (you can
   read more about the builder at https://github.com/ardnt/vercel-python-wsgi)
3. `"config": { "maxLambdaSize": "15mb" }` ups the limit on the size of the code blob passed to
   lambda (Django is pretty beefy)
4. `"routes": [ ... ]` tells Now to redirect all requests (`"src": "/(.*)"`) to our WSGI
   application (`"dest": "maanaim_campanhas/wsgi.py"`)


#### Add Django to requirements.txt

The `vercel-python-wsgi` builder will look for a `requirements.txt` file and will
install any dependencies found there, so we need to add one to the project:
```
# requirements.txt
Django==2.2.4
```


#### Update your Django settings

First, update allowed hosts in `settings.py` to include `.now.sh`:
```python
# settings.py
ALLOWED_HOSTS = ['.vercel.app']
```

Second, get rid of your database configuration since many of the libraries Django may attempt to
load are not available on lambda (and will create an error when python can't find the missing
module):
```python
# settings.py
DATABASES = {}
```


### Deploy

With now installed you can deploy your new application:
```
$ vercel
Vercel CLI 21.3.3
? Set up and deploy “vercel-django-maanaim-campanhas”? [Y/n] y
...
? In which directory is your code located? ./
...
✅  Production: https://vercel-django-core.vercel.app [copied to clipboard] [29s]
```

Check your results in the [Vercel dashboard](https://vercel.com/dashboard).

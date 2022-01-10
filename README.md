# django-ws-include

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/django-ws-include/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Include your templates asynchronously and load their contents using websockets.

# Installation

## Using pip

[This package is in pypi](https://pypi.python.org/pypi/django-ws-include) so you only have to write:

```sh
pip install django-ws-include
```

## Installation in your Django project

Include channels and ws_include in your project's **settings.py**:

```sh

INSTALLED_APPS = [
    ## ...
    'channels',
    'ws_include',
]

```

## Create asgi.py file with django-ws-include routes

```python
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from ws_include.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

```

# Use

Load the **ws_include** template tags at the top of your file and use the **ws_include**
template tag as a replacement of the django include template tag.

You have to pass the local context explicitly to the async included templates, so you can pass all variables you
need in your included template as named parameters of the **ws_include** template tag.

```html

{# Load the ws_include template tag at the top of your template file #}
{% load ws_include %}

{# Call the ws_include template tag indicating what objects needs to replace it #}
{% ws_include "<path of the >" <object1_name>=<object1> <object2_name>=<object2> ... <objectN_name>=<objectN>  %}
```

There is also a repository with a full example that also uses django-async-include:
[django-async-include-example](https://github.com/diegojromerolopez/django-async-include-example).

## Warning and limitations
See [django-async-include](https://github.com/diegojromerolopez/django-async-include) warnings and limitations.

## Examples

### Passing an object

```html
{% load ws_include %}

{# .. #}

{# Load the template and informs the board object is required for the included template  #}
{% ws_include "boards/components/view/current_percentage_of_completion.html" board=board %}
```

### Passing a QuerySet

```html
{% load ws_include %}

{# .. #}

{% ws_include "boards/components/view/summary.html" board=board member=member next_due_date_cards=next_due_date_cards %}
```

# Customization

## Spinner

Overwrite **async_include/spinner.html** template if you want to change the spinner from fontawesome
one (default) by a background image or an image. Otherwise, make sure you are loading fontawesome fonts.

Note that the spinner must have class **async_included-spinner**. Otherwise, the spinner behavior
is going to be unpredictable.

### Show/Hide spinner

Including the optional parameter **spinner__visible=False** when calling the ws_include template tag
will not show the spinner block.

```html
{% load ws_include %}

{# .. #}

{# Will not show the spinner #}
{% ws_include "boards/components/view/last_comments.html" board=board spinner__visible=False %}
```

### Customize spinner template per ws_include template tag call

Use the optional parameter **spinner__template_path** to set a different template path for a
specific ws_include call in your templates.

```html
{% load ws_include %}

{# .. #}

{# Will not show the spinner #}
{% ws_include "boards/components/view/last_comments.html" board=board spinner__template_path="templates/comments/last_comments_spinner.html" %}
```

Remember the spinner tag should contain the **ws_included-spinner** class.

## Block wrapper html tag

Wrapper tag is **div** and maybe you don't want that. Set **html__tag** optional parameter to the name of
the tag you need in that particular context.

Example:

```html
{% load ws_include %}

{# .. #}

{# Will be replaced by <li></li> block instead of <div></div> #}
{% ws_include "boards/components/view/last_comments.html" board=board html__tag='li' %}
```

## Block wrapper html tag class

Customize the wrapper class by passing **html__tag__class** optional parameter to the template tag.

```html
{% load ws_include %}

{# .. #}

{# Will be replaced by <li></li> block instead of <div></div> #}
{# Class last_comments will be added to wrapper class #}
{% ws_include "boards/components/view/last_comments.html" board=board html__tag='li' html__tag__class='last_comments' %}
```

# TODO
* Tests

# Main author
Diego J. Romero-López is a Software Engineer based on Madrid (Spain).

This project is in no way endorsed or related in any way to my past or current employers.
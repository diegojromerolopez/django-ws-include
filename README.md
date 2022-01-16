# django-ws-include

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/django-ws-include/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/django-ws-include.svg)](https://pypi.python.org/pypi/django-ws-include/)
[![PyPI version django-ws-include](https://badge.fury.io/py/django-ws-include.svg)](https://pypi.python.org/pypi/django-ws-include/)
[![PyPI status](https://img.shields.io/pypi/status/django-ws-include.svg)](https://pypi.python.org/pypi/django-ws-include/)
[![PyPI download month](https://img.shields.io/pypi/dm/django-ws-include.svg)](https://pypi.python.org/pypi/django-ws-include/)
[![Maintainability](https://api.codeclimate.com/v1/badges/25ec3d6c327ca2ef3ea1/maintainability)](https://codeclimate.com/github/diegojromerolopez/django-ws-include/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/25ec3d6c327ca2ef3ea1/test_coverage)](https://codeclimate.com/github/diegojromerolopez/django-ws-include/test_coverage)

Include your templates asynchronously and load their contents using websockets
in [Django](https://www.djangoproject.com/).

[See this library in github](https://github.com/diegojromerolopez/django-ws-include).

## How does this work?

This library includes javascript code in the **ws_include** template_tag
and a static javascript file
[ws_include.js](/ws_include/static/ws_include/ws_include.js) file

That javascript code opens a websocket connection (WS_INCLUDE_WEBSOCKET)
that will send a websocket message including the encrypted query and the block ID of
the template that must be loaded asynchronously.

Later, the server responds with the rendered template and the corresponding block ID.
The javascript code uses the block ID to identify were to include the rendered template.

This project is an optimization of
[django-async-include](https://github.com/diegojromerolopez/django-async-include/),
project that while has the same philosophy, it uses HTTP requests to get the
rendered templates, so it is less efficient than using a lone websocket connection.
You are encouraged to take a look to that project to help you understand the aim
of this project.

## Installation

[This package is in pypi](https://pypi.org/project/django-ws-include/).
Use pip to install it:

```shell
pip install django-ws-include
```

### Installation in your Django project

Include channels and ws_include in your project's **settings.py**:

```sh

INSTALLED_APPS = [
    ## ...
    'channels',
    'ws_include',
]

```

### Create asgi.py file with django-ws-include routes

```python
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from ws_include.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

```

Add the static file to the header of your HTML base template file:

```html
<script type="text/javascript" src="{% static 'ws_include/ws_include.js' %}"></script>
```

## Use

Load the **ws_include** template tags at the top of your template and use the **ws_include**
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

### Warning and limitations

#### Object dynamic attributes
No dynamic attribute will be passed to the templates given that only a reference to it is passed
from the caller to the included template callee.

**Don't use dynamic attributes inside an async_included template**.

However, the full object will be passed to the template,
so you could call its methods and properties without any problem.

#### QuerySets
Each QuerySet is passed as encrypted SQL and converted on the receiver to a RawQuerySet.

Note that RawQuerySets have no len method so length filter returns always 0.

**Load ws_included_length in your template and use the filter **ws_included_length** to get the length.

````html
{# Partial HTML template file to be loaded by websockets #}
{% load ws_included_length %}

<div>
    <h2>Product list (items|ws_included_length)</h2>
    <ul>
        {% for item in items %}
        <li>
            {{ item.name }}
        </li>
        {% endfor %}
    </ul>
</div>
````

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

## Customization

### Block wrapper html tag

Wrapper tag is **div** and maybe you don't want that. Set **html__tag** optional parameter to the name of
the tag you need in that particular context.

Example:

```html
{% load ws_include %}

{# .. #}

{# Will be replaced by <li></li> block instead of <div></div> #}
{% ws_include "boards/components/view/last_comments.html" board=board html__tag='li' %}
```

### Block wrapper html tag class

Customize the wrapper class by passing **html__tag__class** optional parameter to the template tag.

```html
{% load ws_include %}

{# .. #}

{# Will be replaced by <li></li> block instead of <div></div> #}
{# Class last_comments will be added to wrapper class #}
{% ws_include "boards/components/view/last_comments.html" board=board html__tag='li' html__tag__class='last_comments' %}
```

## TODO
* More tests: test the Websocket Consumer code.
* Improve documentation.

## Main author
Diego J. Romero-López is a Software Engineer based on Madrid (Spain).

This project is in no way endorsed or related in any way to my past or current employers.

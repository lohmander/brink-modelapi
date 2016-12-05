# CRUD APIs for Brink models

## Installation

```python
INSTALLED_APPS = [
    "brink_modelapi",
    ...
]
```
## Usage

```python
# api.py

from brink_modelapi import ModelAPI
from myproj.models import MyModel

api = ModelAPI()
api.register("mymodels", MyModel,
    operations=["list", "detail", "update", "create", "delete"])
```

and in your urls file

```python
# urls.py

from brink.urls import GET
from myproj.api import api

urls = [
    *api.urls,
    # other urls...
]
```

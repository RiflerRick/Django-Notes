# Custom User Models

Everytime we create a django project a User model is actually created by default with some attributes, that user model is responsible for actually managing authentication as well. Django itself can manage the authentication of all its users, we ideally do not need to write the authentication layer of django. However we may want to use this same authentication layer of django but with a more customized user model than the one provided by django. This is handled by creating a separate user model.

`models.py`
```python
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser
	)
# Whenever we are trying to create a custom user model the way to create that is to use an AbstractBaseUser. 
# This 


```
# Custom User Models

Everytime we create a django project a User model is actually created by default with some attributes, that user model is responsible for actually managing authentication as well. Django itself can manage the authentication of all its users, we ideally do not need to write the authentication layer of django. However we may want to use this same authentication layer of django but with a more customized user model than the one provided by django. This is handled by creating a separate user model.


Whenever we are trying to create a custom user model, we have to import AbstratBaseUser because it actually gives us the authentication based functionality which we can modify as we see fit. We cannnot use `models.Model` here because then we would have to write the entire functionality of authentication ourselves.

AbstractBaseUser actually contains 3 fields: **id, password and last_login** 

`models.py`
```python
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser
	) 

class CustomUser(AbstractBaseUser):
	pass

```
Simply writing this model would actually create a CustomUser model with 3 attributes id, password and last_login

Instead of using CustomUser as the class name in case of the custom user model we can rename it to User as this is indeed the User class that we are going to use. The django documentation says MyUser but thats okay. This is simply completely getting rid of the django User class by calling my custom user model as User. 


`models.py`
```python
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser
	) 

class CustomUser(AbstractBaseUser):
	email 		= models.EmailField(unique=True, max_length=255)	
	full_name	= models.CharField(max_length=255, blank=True, null=True)
	active 		= models.BooleanField(default=True) # active simply means whether the user can login
	staff 		= models.BooleanField(default=False) # staff user
	admin 		= models.BooleanField(default=False) # superuser

	# now we want the email field to be my username field. Here his how to let Django know that email would
	# be my username field or the field that is going to uniquely identify that user

	USERNAME_FIELD = "email" 

	# after this we need to specify which are the fields that we are going to require.
	# required fields are the fields that will come up when we want to add users from the console using 
	# manage.py 	 

	REQUIRED_FIELDS = ["full_name", "email"]

	def __str__(self):
		# this is the function that defines how a object will be displayed when it is printed
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	# Note that the get_full_name and get_short_name functions are actually required there for the purpose of 
	# identifying the users. Its basically a way that Django identifies the users

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_active(self):
		return self.is_active



```

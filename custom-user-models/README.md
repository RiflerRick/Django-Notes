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

One important idea to note here is that for the custom user model we actually do not need to define all the properties of the user in one place. We can have a separate model for handling the user details and that model can actually extend the user model with new attributes

## User Model Manager

A Model Manager is actually used creating users and the like. For this we need to import `BaseUserManager` from django.contrib.auth.models


`models.py`
```python
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
	) 

class UserManager(BaseUserManager):
	def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
		# here we are taking only the required arguments as the parameter
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Password is required")
		user = self.model(
			email = self.normalize_email(email) 
			# normalize is a built-in function that normalizes the email address, in this case 
			# it simply changes to domain part of the email address to lowercase

		)	
		user.set_password(password) # thats also how to change the password
		user.staff = is_staff
		user.admin = is_admin
		user.active = is_active
		user.save(using=self._db) # saving to the database
		return user

	def create_staffuser(self, email, password=None):
		user = self.create_user(
			email,
			password=password,
			is_staff=True
		)
		return user

	def create_superuser(self, email, password=None)
		user = self.create_user(
			email,
			password=password,
			is_staff=True,
			is_admin=True
		)
		return user		


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

	REQUIRED_FIELDS = ["full_name"] 
	# note that actually email is the username field so obviously it is a required field however since 
	# it is already mentioned as the username field we do not need to explicitly say that email is a required # field.

	objects = UserManager() # this actually declares the model manager for this model

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
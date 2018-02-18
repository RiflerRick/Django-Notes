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

We need to change the built in user model to ours
For this we need to add a new variable to the settings.py file 

`AUTH_USER_MODEl = 'app1.User'`

app1 is actually the name of the app where that User model exists

**Note**: When we are dealing with a custom user model we may run into problems after creating migration files and migrating the models. Such problems might arise due to a change in the user model to be referenced especially if there is data already present in the original user model. To handle such issues and many others in general we might need to use the concept of fixtures to take the dump of the entire data in json or any other format and store it somewhere. This might also help when we are trying to migrate databases

The command for taking fixtures is the following:
`python manage.py dumpdata products.Product --format json --indent 4 > products/fixtures/products.json`

`dumpdata` is the command
`products.Product`- products is the name of the app and Product is the name of the model

`--format json` will format the output in terms of json

`--index 4` basically json indent 4

Now for loading the data to a new database, we obviously need to change the name of the database in the settings file. 

`python manage.py loaddata products/fixtures/products.json`

`loaddata` is the command for loading the data from the fixture json file that is given

There are 2 other functions that need to be defined inside the custom user model

```python
def has_perm(self, perm, obj=None):
	return True

def has_module_perms(self, app_label):
	return True
```

These are basically 2 different permission based functions that need to be defined

Inside the admin file of the app we need to register the model if we want that model to be accessible from the admin page

`admin.py`
```python
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
```

## User Admin

Note that when we are building a model we might want to change the way in which an admin can see the model or make changes to the data in the model(basically edit the model). Here is how we can do that from the `admin.py` page.

`admin.py`
```python

from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
	search_fields = ['email']
	class Meta:
		model = User

admin.site.register(User, UserAdmin) 

```

That class `UserAdmin` will actually include a search field for the email. We can obviously do stuff like that from the admin page itself

So for customizing this even more we can actually add custom forms in the `forms.py` file
```python

class UserAdminCreationForm(forms.ModelForm):
	"""
	this is like a simple form that will be displayed for User creation in the admin page
	"""
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email') # this part is essentially the required fields

	def clean_password2(self):
		"""
		clean_<field_name> function is called by django internally in order to clean the field value
		"""
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserAdminChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = User
		fields = ["email", "password", "active", "admin"]

	def clean_password(self):
		return self.initial["password"]

```
So basically what we just did here is created some custom forms for the admin page and changed what are the fields that the admin page is going to have for making changes to one entry of the model. Note that this is very important to understand. Here we are not changing how the listing on the admin page is going to be done for a particular model. Here we are simply concerned about what will be the fields when we make changes to one record or one entry of the model or when we create a new record or entry of the model.

Now on the admin page we can write code for actually making changes to the way the model listing will look like. We can do that in the following way

`admin.py`
```python
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin)
	form = UserAdminChangeForm # this is the change form
	add_form = UserAdminCreationForm # this is the creation form

	list_display = ('email', 'admin') # this is going to describe how the list is displayed
	list_filter = ('admin', 'staff', 'active') # this is going to describe what filters we are going to use

	# fieldsets are the fields to be present in the change form
	fieldsets = (
		(None, {'fields':('email', 'password')}), # here basically we would get the 
		('Personal_info', {'fields':()}),
		('Permissions', {'fields':('admin', 'staff', 'active')})	
	)

	# add_fieldsets are the fields to be present in the add form
	add_fieldsets = (
		(None, {
				'classes': ('wide'),
				'fields': ('email', 'password1', 'password2')
			}
		)
	)

	search_fields = ('email')
	ordering = ('email')
	filter_horizontal = {}


```



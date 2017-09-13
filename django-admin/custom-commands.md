## Writing Custom commands for Django-admin

Django enables us to write custom commands for django-admin. This is the done in the following way:

The project should have a `management/commands` directory in the application. Now we can write any python module in the commands directory and any module not starting with an underscore becomes a command module.

The `management` module must have an `__init__.py` file and the `commands` module should also have an `__init__.py` file. 

Any command module must essentially have a `Command` class inheriting the `BaseCommand` class or one of its subclasses.

- Writing to the terminal as output to the command: Instead of directly writing to stdout or stderr we need to use the `self.stdout.write()` method.

 

## Writing Custom commands for Django-admin

Django enables us to write custom commands for django-admin. This is the done in the following way:

The project should have a `management/commands` directory in the **app**. Now we can write any python module in the commands directory and any module not starting with an underscore becomes a command module.

The `management` module must have an `__init__.py` file and the `commands` module should also have an `__init__.py` file. 

Any command module must essentially have a `Command` class inheriting the `BaseCommand` class or one of its subclasses.

- Writing to the terminal as output to the command: Instead of directly writing to stdout or stderr we need to use the `self.stdout.write()` method.

### Overriding Commands
Django registers the built in commands and then searches for the commands in the INSTALLED_APPS in reverse. During the search if a duplicate command is found the previous command is overwritten. Basically for this to happen the commnd must have the same nameand its app should be before the new app that is overwriting it. 

- Implementing the `handle()` method. If we wanna subclass the `BaseCommand` class we would have to implement the `handle()` method ourselves.

### `BaseCommand.execute(*args, **options)`
Tries to execute the current command. execute is actually not be called directly from your code, rather use the `call_command()` method.

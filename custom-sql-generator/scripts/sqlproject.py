#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import AppCommand, BaseCommand
from django.db import DEFAULT_DB_ALIAS

from optparse import make_option
from StringIO import StringIO


class Command(BaseCommand):
    help = "Prints the CREATE TABLE SQL statements for all installed apps."

    option_list = AppCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a database to print the '
                'SQL for.  Defaults to the "default" database.'),
    )

    def handle(self, *args, **options):
        sqlproject = StringIO()
        apps = [self._clear_app_name(app) for app in settings.INSTALLED_APPS]
        call_command("sql", *apps, stdout=sqlproject)
        sqlproject.seek(0)
        self.stdout.write(sqlproject.read())

    def _clear_app_name(self, app):
        app_splited = app.split('.')
        # Only the last part of the app name is useful for sql management command
        return app_splited[-1]

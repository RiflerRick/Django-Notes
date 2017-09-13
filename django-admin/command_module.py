from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):
    """
    The BaseCommand class must be inherited and the name of this class must be 
    Command and nothing else.
    """
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        """
        method used for adding required and optional arguments to the command
        For instance if we use simply parser.add_argument method we will be
        adding required arguments.
        """
        parser.add_argument("poll_id", nargs="+", type=int)
        # for adding optional arguments here is how we can do that. This option 
        # will also be available in the options dictionary of the handle method
        parser.add_argument("--delete", action="store_true", dest="delete", default=False, help="Delete poll instead of closing it")

    def handle(self, *args, **options):
        """
        This method is essentially called for processing. The arguments passed 
        with the command are available as dictionary entries of options argument
        in this method. 
        """
        for poll_id in options["poll_id"]:
            try:
                poll = Poll.object.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()
            
            # for writing anything to stdout we use self.stdout.write and do not
            # directy write anything
            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'% poll_id))

        # By default BaseCommand.execute() method deactivates translations 
        # because some commands shipped with Django perform several tasks that 
        # require a project-neutral string language.
        # However if our code requires some locale we need to manually activate
        # it in the following way.
        from django.utils import translation

        translation.activate('ru')

        # or import from settings
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)
        """
        Whatever we need to perform with the locale
        """
        translation.deactivate()
        # If we want to leave the translation as it is and do not wanna deactivate it we can do so using the following option
        # To do this we need to use the BaseCommand.leave_locale_alone option. However make sure that the USE_I18N setting
        # is always on while runnning the command.





        

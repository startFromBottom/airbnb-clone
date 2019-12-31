from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):

        admin = User.objects.get_or_none(username="ebadmin")

        if admin is None:
            User.objects.create_superuser("ebadmin", "uhh0701@gmail.com", "sch0807!!")
            self.stdout.write(self.style.SUCCESS("Superuser Created!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists!"))

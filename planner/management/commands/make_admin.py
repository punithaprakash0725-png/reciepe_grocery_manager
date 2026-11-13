from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Give an existing user admin access: python manage.py make_admin <username>"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, *args, **opts):
        User = get_user_model()
        try:
            user = User.objects.get(username=opts["username"])
        except User.DoesNotExist:
            raise CommandError(f"No user named {opts['username']!r}")
        user.is_staff = user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"{user.username} is now an admin."))

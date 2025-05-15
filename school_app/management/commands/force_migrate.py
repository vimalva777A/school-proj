from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Force migrations on Render"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Applying migrations..."))
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        self.stdout.write(self.style.SUCCESS("Migrations applied successfully."))


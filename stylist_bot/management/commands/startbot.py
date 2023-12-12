from django.core.management.base import BaseCommand
from stylist_bot.bot import start_bot  # Import your bot logic from another file

class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        # Call the function from your bot logic to start the bot
        start_bot()

        self.stdout.write(self.style.SUCCESS('Bot started successfully'))
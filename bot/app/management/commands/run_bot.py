from django.core.management.base import BaseCommand
from app.bot import bot


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        bot.polling()

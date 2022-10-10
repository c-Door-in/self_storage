from datetime import datetime
from django.core.management.base import BaseCommand
from environs import Env
from store.models import Box
import time


class Command(BaseCommand):
    help = "Expired boxes reminder"

    def handle(self, *args, **kwargs):
        env = Env()
        env.read_env()

        interval = 60*60*24
        while True:
            now = datetime.now()
            boxes = Box.objects.filter(rental_end_time__gt=now)
            for box in boxes:
                expires_in = box.rental_end_time - now
                if expires_in.days in (1, 7, 14):
                    # send message
                    pass
            time.sleep(interval)

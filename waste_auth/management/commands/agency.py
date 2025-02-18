
# import uuid
from django.core.management import BaseCommand
from account.helpers.reusable import generate_account_number



class Command(BaseCommand):
  help = ""
  
  def handle(self, *args, **options):
    test = generate_account_number()

    print(test)
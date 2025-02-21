import random

def generate_account_number():
    """
    Generate a random account number for a user.
    """
    # account_number = random.randint(1000000000, 9999999999)
    account_number= random.randint(10**9, 10**10 - 1)
    return account_number
import random
import string
import time


def get_random_str(k):
    return "".join(random.choices(string.ascii_letters, k=k))


def get_random_digits(k):
    return "".join(random.choices(string.digits, k=k))


def now():
    return int(time.time() * 1000)

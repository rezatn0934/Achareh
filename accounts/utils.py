import random
import string
from django.core.cache import caches
from django.core.validators import RegexValidator

phoneNumberRegex = RegexValidator(regex=r"^09\d{9}$")


def generate_random_digits(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def set_to_redis(key: str, value: str, database: str):
    try:
        caches[database].set(key, value=value)
        return True
    except Exception as e:
        return str(e)


def get_from_redis(key, database):
    if cache_value := caches[database].get(key):
        return cache_value


def send_otp(otp):
    """
    this function just print random digits
    :param otp:
    :return:
    """
    print('otp code is {}'.format(otp))

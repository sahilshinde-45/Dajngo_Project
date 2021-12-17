from enum import IntEnum
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class Status (IntEnum):

    one = 1
    zero = 0

    @classmethod 
    def choices(cls):
        return [(key.value,key.name)for key in cls]


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self,user,timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()
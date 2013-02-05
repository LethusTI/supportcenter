# -*- coding: utf-8 -*-

__all__ = ('CaptchaStore',)

import random
import datetime
import time
import unicodedata

from django.conf import settings

from mongoengine import *

from .constants import *

# Heavily based on session key generation in Django
# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange

try:
    import hashlib  # sha for Python 2.5+
except ImportError:
    import sha  # sha for Python 2.4 (deprecated in Python 2.6)
    hashlib = None

MAX_RANDOM_KEY = 18446744073709551616L     # 2 << 63

class CaptchaStore(Document):
    hashkey = StringField(primary_key=True)
    response = StringField(required=True)
    expiration = DateTimeField()

    meta = {'allow_inheritance': False,
            'db_alias': 'tmp',
            'collection': 'captcha_store',
            'ordering': ['created'],
            'indexes': [
               {'fields': ['expiration']}
            ]}

    @classmethod
    def get_safe_now(cls):
        try:
            from django.utils.timezone import utc
            if settings.USE_TZ:
                return datetime.datetime.utcnow().replace(tzinfo=utc)
        except:
            pass
            
        return datetime.datetime.now()
    
    @classmethod
    def generate_new_response(cls):
        chars = []
        
        for i in range(CAPTCHA_LENGTH):
            chars.append(random.choice(CAPTCHA_CHARS))
        
        return ''.join(chars).upper()
    
    @classmethod
    def generate_new_item(cls):
        obj = cls()
        obj.response = cls.generate_new_response()

        obj.expiration = (
            cls.get_safe_now() +
            datetime.timedelta(minutes=CAPTCHA_TIMEOUT))

        key = unicodedata.normalize(
                'NFKD', str(randrange(0, MAX_RANDOM_KEY)) +
                str(time.time()) +
                obj.response)

        if hashlib:
            obj.hashkey = hashlib.sha1(key).hexdigest()
        else:
            obj.hashkey = sha.new(key).hexdigest()
        
        obj.save()

        return obj

    @classmethod
    def remove_expired(cls):
        cls.objects(expiration__lte=cls.get_safe_now()).delete()

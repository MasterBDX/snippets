import random
import string
import os
from django.utils.text import slugify
from . import models


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    '''
        Will return random generated string 
        that have size = size kwarg and content from chars kwarg
    '''
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    '''
        Will return unique generated slug it slug was not unique 
        will continue regenerate until get unique slug
    '''
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.username)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=5)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

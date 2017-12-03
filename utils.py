import time
from functools import wraps
from config import DEBUG


def timer(fxn):
    if not DEBUG:
        return fxn

    @wraps(fxn)
    def _(*args, **kwargs):
        start = time.time()
        result = fxn(*args, **kwargs)
        dt = time.time() - start
        print("{}: {:0.4f}s".format(fxn.__name__, dt))
        return result
    return _

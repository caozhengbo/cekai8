from cekai8.settings import SECRET_KEY
import hashlib, base64
import time, random
import uuid


def md5(s):
    h = hashlib.md5()
    h.update(s.encode(encoding='utf-8'))
    return h.hexdigest()


def random_key():
    return md5(str(time.time()) + str(random.randint(0, 1000)))


def encryption(s):
    h = hashlib.md5()
    h.update(SECRET_KEY.encode('UTF-8'))
    h.update(s.encode('UTF-8'))
    result = base64.b64encode(h.hexdigest().encode('UTF-8')).decode('UTF-8')
    return result

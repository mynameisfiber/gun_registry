import bcrypt
import os


if os.getenv('ENV') == 'DEV':
    DEBUG = True
    GUN_SALT = bcrypt.gensalt(rounds=4)
    SCRYPT_ENC_PARAMS = {
      'maxtime': 0.1,
      'maxmemfrac': 0.1,
    }
else:
    DEBUG = True
    GUN_SALT = bcrypt.gensalt(rounds=18)
    SCRYPT_ENC_PARAMS = {
       'maxtime': 120,
       'maxmem': int(64e6),  # 64 MB
    }

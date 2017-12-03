import scrypt
import bcrypt
import pickle

from utils import timer
from config import GUN_SALT, SCRYPT_ENC_PARAMS


class Record(object):
    def __init__(self, gunid, **metadata):
        if isinstance(gunid, str):
            gunid = gunid.encode('utf8')
        elif isinstance(gunid, int):
            gunid = str(gunid).encode('utf8')
        self.gunid = gunid
        self.metadata = metadata

    def __getitem__(self, key):
        return self.metadata[key]

    @timer
    def dec_metadata(self, enc_meta):
        key = self.gunid
        meta_pkl = scrypt.decrypt(enc_meta, key, encoding=None)
        self.metadata = pickle.loads(meta_pkl)
        return self

    @timer
    def enc_gunid(self):
        data = self.gunid
        return bcrypt.hashpw(data, GUN_SALT)

    @timer
    def enc_metadata(self):
        key = self.gunid
        data = pickle.dumps(self.metadata)
        return scrypt.encrypt(data, key, **SCRYPT_ENC_PARAMS)

import gunregistry as gr
import string
import random

gr.SCRYPT_PARAMS = {
    'maxtime': 1,
    'maxmemfrac': 0.01,
}


def test_put_get():
    metadata = {"key": "".join(random.sample(string.ascii_letters, 24))}
    gunid = random.randint(0, 99999)

    db = gr.Database()
    db.add_record(gunid, **metadata)
    assert next(db.get_record(gunid))['key'] == metadata['key']

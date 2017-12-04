import gun_registry as gr
import string
import random


def test_put_get():
    metadata = {"key": "".join(random.sample(string.ascii_letters, 24))}
    gunid = random.randint(0, 99999)

    db = gr.GunRegistry()
    db.add_record(gunid, **metadata)
    assert gunid in db
    assert next(db.get_records(gunid))['key'] == metadata['key']


def test_put_get_multi():
    db = gr.GunRegistry()

    gunids = []
    for i in range(20):
        gunid = "".join(random.sample(string.ascii_letters, 24))
        metadata = {"check": gunid}
        db.add_record(gunid, **metadata)
        gunids.append(gunid)

    for gunid in gunids:
        assert next(db.get_records(gunid))['check'] == gunid


def test_get_noexist():
    db = gr.GunRegistry()
    try:
        next(db.get_records("NOT_EXIST"))
    except KeyError:
        return
    assert False, "We should have a KeyError"

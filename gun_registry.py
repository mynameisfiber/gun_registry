from record import Record


class GunRegistry(dict):
    def get_records(self, gunid):
        key = Record(gunid).enc_gunid()
        try:
            values = self._get_records(key)
        except KeyError as ex:
            raise KeyError(gunid) from None
        for value in values:
            yield Record(gunid).dec_metadata(value)

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError("__setitem__ not implemented... "
                                  "use add() instead")

    def __contains__(self, gunid):
        key = Record(gunid).enc_gunid()
        return super().__contains__(key)

    def __getitem__(self, gunid):
        return list(self.get_records(gunid))

    def add_record(self, gunid, **metadata):
        record = Record(gunid, **metadata)
        key = record.enc_gunid()
        value = record.enc_metadata()
        self._add_record(key, value)

    def _get_records(self, key):
        return super().__getitem__(key)

    def _add_record(self, key, value):
        super().setdefault(key, []).append(value)

# Secret Gun Registry

America desperately needs a gun registry. This would be a database that tracks a
gun's serial number as it is bought and sold throughout the country. However,
because of strong lobbying powers and 18 U.S.C. 926(a) such a registry isn't
allowed.

Much of the argument against such a registry comes from the thought that it
would help the government disarm citizens if there was ever revolts against
them. However, this concern can be mitigated.

We present a database that has slow and resource intensive retrievals, encrypted
storage and no scanning. This means:

- Transaction information can only be retrieved for known serial numbers
- A full view of the database is not possible without first enumerating all
  serial numbers
- Each retrieval can be forced to take an arbitrary amount of time, thus
  limiting any brute force attack

## How to use

If you just want to play around, import the `GunRegistry` object and have a go!
`config.py` defines the various properties of the database including how
resource intensive each query should be. This resource intensiveness is defined
by bcrypt/scrypt parameters.

To make this a bit more useful, we also include `GunRegistryRedis` and
`GunRegistryCassandra` that store results in Redis or Cassandra.

For the default non-development config values, we can see the following
performance:

```
In [1]: from gun_registry import GunRegistry

In [2]: db = GunRegistry()

# Inserting a record takes 114 seconds!
In [3]: db.add_record("US3249877651X", name='mynameisfiber', timestamp=234234)
enc_gunid: 20.0598s
enc_metadata: 94.7125s

In [4]: db.add_record("US3249877651X", name='someoneelse', timestamp=234236)
enc_gunid: 20.2734s
enc_metadata: 94.6475s

# Each data retrieval takes ~95 seconds plus a 20 second overhead
In [5]: result = list(db.get_records("US3249877651X"))
enc_gunid: 19.9013s
dec_metadata: 97.4017s
dec_metadata: 93.0884s

In [6]: for i in result:
   ...:     print(i['name'])
      ...: 
      mynameisfiber
      someoneelse

# Attempting to read a key that doesn't exist takes ~20 seconds
In [7]: list(db.get_records("RANDOM_ID"))
enc_gunid: 19.8754s
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-10-a2463cf0fa96> in <module>()                              
----> 1 list(db.get_records("RANDOM_ID"))    
                          
/home/micha/playground/gunregistry/gun_registry.py in get_records(self, gunid)
      8             values = self._get_records(key)       
      9         except KeyError:
---> 10             raise KeyError(gunid)
     11         for value in values:
     12             yield Record(gunid).dec_metadata(value)
                                                                           
KeyError: 'RANDOM_ID'  
```

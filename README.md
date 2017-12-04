# Secret Gun Registry

America desperately needs a [gun
registry](https://en.wikipedia.org/wiki/National_Tracing_Center#Computer_Assisted_Retrieval_System_.28CARS.29).
Currently all we have are [paper
records](https://www.vice.com/en_us/article/wdbd9y/the-atfs-nonsensical-non-searchable-gun-databases-explained-392)
which cannot be searched. A gun registry would be a searchable database that
tracks a gun's serial number as it is bought and sold throughout the country.
However, because of [strong lobbying
powers](http://www.washingtonpost.com/wp-dyn/content/article/2010/10/25/AR2010102505823.html)
and [18 U.S.C.
926(a)](http://www.nytimes.com/2012/12/26/us/legislative-handcuffs-limit-atfs-ability-to-fight-gun-crime.html)
such a registry isn't allowed.

Much of the [argument against such a
registry](https://www.nraila.org/issues/registration-licensing/) comes from the
thought that it would help the government disarm citizens if there was ever
revolts against them. However, this concern can be mitigated.

We present a database that has slow and resource intensive retrievals, encrypted
storage and no scanning. These slowdowns and resource requirements are a
fundamental property of the way the data is stored. This means:

- Transaction information can only be retrieved for known serial numbers
- A full view of the database is not possible without first enumerating all
  serial numbers
- Each retrieval can be forced to take an arbitrary amount of time, thus
  limiting any brute force attack
- These properties persist even if the raw data is stolen and analyzed with new
  code.

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

## Config

In `config.py` you'll see the various parameters for setting how resource
intensive the encryption tasks are. Here's a rundown of what they mean:

| Parameter | Meaning |
| --------- | ------- |
| `bcrypt.gensalt(rounds=18)` | This designates how hard it is to do the data lookup (even if the data doesn't exist in the registry). Values range from 4-31 where 4 means the calculation is fast and 31 is incredibly slow. For reference, on my laptop `rounds=4` results in 0.002s per gun id while `rounds=18` results in 20s. Each additional round [roughly doubles](https://security.stackexchange.com/a/83382) the required time. |
| `SCRYPT_ENC_PARAMS['maxtime']` | Maximum time in seconds to encrypt/decrypt the payload of each record. The actual amount of time spent encryption is generally fairly close to this number. |
| `SCRYPT_ENC_PARAMS['maxmem']` | Maximum amount of memory in bytes used to encrypt/decrypt the payload of each record. Actual memory use is generally fairly close to this number |
| `SCRYPT_ENC_PARAMS['maxmemfrac']` | Same as `maxmem` above, but written in terms of a fraction of available memory. |

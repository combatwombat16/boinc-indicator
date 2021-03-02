class _Enum(object):
    UNKNOWN = -1  # Not in original API

    @classmethod
    def name(cls, value):
        """ Quick-and-dirty fallback for getting the "name" of an enum item """

        # value as string, if it matches an enum attribute.
        # Allows short usage as Enum.name("VALUE") besides Enum.name(Enum.VALUE)
        if hasattr(cls, str(value)):
            return cls.name(getattr(cls, value, None))

        # value not handled in subclass name()
        for k, v in cls.__dict__.items():
            if v == value:
                return k.lower().replace('_', ' ')

        # value not found
        return cls.name(_Enum.UNKNOWN)

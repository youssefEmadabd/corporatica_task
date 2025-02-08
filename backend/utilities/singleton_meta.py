from typing import Type, Dict, Any
from abc import ABCMeta as AbstractMeta

class SingletonMeta(AbstractMeta):
    """ A thread-safe Singleton metaclass. """
    _instances: Dict[Type, Any] = {}
    _init_args: Dict[Type, tuple] = {}  # Store init args

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._init_args[cls] = (args, kwargs)  # Store init args
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            # Ensure __init__ is called only once per class
            if not hasattr(cls._instances[cls], "_initialized"):
                init_args, init_kwargs = cls._init_args[cls]
                cls._instances[cls].__init__(*init_args, **init_kwargs)
                cls._instances[cls]._initialized = True  # Mark as initialized
        return cls._instances[cls]
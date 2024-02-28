class SingletonMeta(type):
    """
    单例元类

    继承了 type 类，这使它成为一个元类。元类是用于创建类的类，它控制着类的创建过程。
    _instances 是一个字典，用于存储每个类的实例。
    __call__ 是元类中的一个特殊方法，当我们创建一个类的实例时，__call__ 方法会被调用。
    在这里，__call__ 方法用于控制实例的创建。它检查 _instances 字典中是否已经有了该类的实例，如果没有，就通过 super().__call__(*args, **kwargs) 创建一个新的实例，并将其存储在 _instances 字典中；如果已经存在，就返回已有的实例。
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    pass

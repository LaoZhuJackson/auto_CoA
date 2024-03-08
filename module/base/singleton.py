"""
这段代码的作用是创建一个元类 SingletonMeta，它能够确保每个继承了它的类只有一个实例。
Singleton 类是一个使用了这个元类的示例，使得它成为一个单例类。
"""


class SingletonMeta(type):
    """
    单例类元类

    它继承了 type 类，这使它成为一个元类。元类是用于创建类的类，它控制着类的创建过程。

    __instances 是一个字典，用于存储每个类的实例。

    __call__ 是元类中的一个特殊方法，当我们创建一个类的实例时，__call__ 方法会被调用。
    在这里，__call__ 方法用于控制实例的创建。它检查 __instances 字典中是否已经有了该类的实例，
    如果没有，就通过 super().__call__(*args, **kwargs) 创建一个新的实例，并将其存储在 __instances 字典中；
    如果已经存在，就返回已有的实例。
    """

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    单例类基类

    这是一个使用 SingletonMeta 元类的类。
    通过使用 metaclass=SingletonMeta，我们告诉 Python 在创建这个类时使用 SingletonMeta 作为元类，从而使用了上述的单例逻辑。

    其他单例类仅需继承该类即可。
    """

    pass

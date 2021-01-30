class Father(object):
    def foo(self):
        raise NotImplementedError()
    def bar(self):
        raise NotImplementedError()

class SubClass(Father):   #繼承Father類別，雖然沒有繼承到bar、所有father的方法，仍能被成功實例化
    def foo(self):
        return 'foo() called'

a = SubClass()
a.foo()
a.bar()  # NotImplementedError



################
from abc import ABCMeta, abstractmethod
class Base(metaclass=ABCMeta): #抽象類別，確保後續實例化的物件都要有抽象的方法，否則實例失敗
    @abstractmethod
    def foo(self):
        pass
    @abstractmethod
    def bar(self):
        pass

class Concrete(Base):
    def foo(self):
        pass

c = Concrete() # TypeError
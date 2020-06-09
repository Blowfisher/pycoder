#抽象类 用于规定子类方法的作用又给子类自由发挥的空间 前提就是子类中一定要实现抽象类定义的抽象方法

from abc import ABCMeta,abstractmethod
class A(metaclass=ABCMeta):
  def __init__(self,name,a,b):
    self.name = name
    self.__a = a
    self.__b = b
  @abstractmethod
  def ptr_name(self):
    pass
  def ptr_info(self):
    print('a is {0},b is {1} '.format(self.__a,self.__b))


class B(A):
  def __init__(self,name,age,sex):
    super().__init__(name,age,sex)

  def ptr_name(self):
    print('{0} age is {0}'.format(self.name,self.age))


if __name__ == '__main__':
  test = B('Bambo',18,'male')
  test.ptr_info()
  print(test.name)
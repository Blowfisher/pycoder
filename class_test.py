from abc import ABCMeta,abstractmethod

#异常定义
class NoHeating(Exception):
    "Simulate the alcohol lamp does not work"
    def __init__(self,state):
        super(NoHeating, self).__init__()
        self.state = state

class Human(metaclass=ABCMeta):
    def __init__(self,name,age,address,mary):
        self.__name = name
        self.__age = age
        self.__address = address
        self.__mary = mary
    def get_name(self):
        return  self.__name
    def get_age(self):
        return  self.__age
    def get_address(self):
        return  self.__address
    def get_summary(self):
        return  self.__mary
    @abstractmethod
    def ptr_info(self):
        pass

class Teacher(Human):
    def __init__(self,name,age,address,summary,money,*args):
        super().__init__(name,age,address,summary)
        self.__money = money
        self.classor = args
        self.name = super().get_name()
    def ptr_info(self):
        print('{0} is a teacher'.format(self.name))

    def get_address(self):
        self.address = super().get_address()
        choice = input('Tearcher {0} Are you desired to tell us about your address? y/n'.format(self.name))
        if choice == 'y':
            self.address = super().get_address()
            print('Teacher {0}\'s address is: {1}'.format(self.name,self.address))
        else:
            print('Tearcher {0} do\'t want to tell us about her address.'.format(self.name))

    def get_classor(self):
        print('Teacher {0} teaching {1}'.format(self.name,self.classor))

    def get_money(self):
        print(type(self.__money))
        state = "exhausted"
        try:
            if self.__money < 25000:
                raise NoHeating(state)
        except NoHeating as nh:
            print('{0}\'s money is low'.format(self.name))
        else:
            print('Teacher {0}\'s money is {1}'.format(self.name,self.__money))
        finally:
            print('Finally--------------------')



if __name__ == '__main__':
    bambo = Teacher('Bambo',28,'湖南省隆回县七江乡白云村',2,200000,'English','语文','math')
    bambo.ptr_info()
    bambo.get_classor()
    bambo.get_money()
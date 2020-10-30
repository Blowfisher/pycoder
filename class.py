class Robot(object):
  num = 0
  def __init__(self,stype):
    self.type = stype
    Robot.num += 1
    print('Initializing {0} {1}'.format(self.type,Robot.num))

  @property
  def work(self):
    "simulated robot is working,wear and tear"
    print('%s Robot is working' %self.type)
  @work.setter
  def set_work(self,value):  
     pass
  @work.deleter
  def del_work(self):
    pass
    
  def destroy(self):
    print('%s Robot is being destoryed !'%self.type)
    Robot.num -= 1
    if Robot.num == 0:
      print('Robots are destroyed.')
    else:
      print('There are still %d'%Robot.num)

  @classmethod
  def print_num(cls):
    print("There are %d robots"%cls.num)
  @staticmethod
  def print():
     print('xxxx')

class Sweepor(Robot):
  def __init__(self,type,age,expect):
    super(Sweepor,self).__init__(type)
    self.age = age
    self.expect = expect

  def print_type(self):
    print(self.type)
#``````````````````````````````````````
#``````````````````````````````````````
# #``````````````````````````````````````

class base1(object):
  def __init__(self):
    print("base1 class")

class A(base1):
  def __init__(self):
    base1.__init__(self)
###################################################################
###################################################################
###################################################################
class Conical_section(object):
  def __init__(self,name):
    self.name = name
    print('Determine the name of the curve: {0}'.format(name))
  def ptr_equation(self):
    print('Output {0} equation'.format(self.name))

class Ellipse(Conical_section):
  def __int__(self,name,a,b):
    Conical_section.__init__(self,name)
    self.a = a
    self.b = b

  def ptr_eccentricity(self):
    print('the eccentricity of this ellips is {0}'.format((1-self.b**2/self.a**2)**0.5))
  def prt_equation(self):
    super(Ellipse,self).ptr_equation()
    print("x^2/{0}+y^2/{0}^2=1".format(self.a,self.b))

class Paracurve(Conical_section):
  'This class is used to simulate paracurve'
  def __init__(self,name,p):
    Conical_section.__init__(self,name)
    self.p = p
  def ptr_equation(self):
    Conical_section.ptr_equation(self)
    print('y^2={0}*x'.format(2*self.p))
if __name__ == '__main__':
  a = Sweepor('Err',16,'happy')
  a.print_type()




from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import MySQLdb as mysql

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://bambo:redhat@192.168.16.103:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
#new_user = User(id='8', name='jay')
# 添加到session:
#session.add(new_user)
# 提交即保存到数据库:
#session.commit()

user = session.query(User).all()
#print(user.name)
print(user)

# 关闭session:
session.close()
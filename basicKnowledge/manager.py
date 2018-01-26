#-*- encoding=UTF-8 -*-
from flask_script import Manager
from basicKnowledge.flaskTest import app

manager = Manager(app)

@manager.option('-n','--name',dest = 'name', default = 'nowcoder')
def hello(name):
    print 'hello', name

@manager.command
def initialize_database():
    print 'database....'
    '''初始化数据库'''



##便于统一管理

if __name__ == '__main__':
    manager.run()

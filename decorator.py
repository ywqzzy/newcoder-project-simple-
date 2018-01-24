#-*- encoding=UTF-8 -*-


def log(level,*args, **kvargs):
    '''
    * 无名
    ** 有名
    '''
    def inner(func):
        def wrapper(*args, **kvargs):
            print level,'before calling', func.__name__
            func(*args, **kvargs)
            print level,'after calling', func.__name__
        return wrapper
    return inner

@log(level = 'INFO')
def hello():
    print 'hello'

@log(level='xxx')
def hello2(name):
    print 'hello', name

if __name__ == '__main__':
    hello2('hahahah')
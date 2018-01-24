#-*- coding: UTF-8 -*-

def demo_string():
    stra = "hello world"
    print stra.capitalize()
    print stra.replace('world', 'newcoder')
    strb = '\n\r hello world \r\n'
    print strb.lstrip()
    print stra.startswith('hello')
    print stra.endswith('wordl')
    print stra + strb.lstrip()
    print len(stra)
    print '...'.join(['a', 'b', 'c'])

def demo_operation():
    pass

def demo_buildinfunction():
    print max(1001, 1), min(1001, 1)
    print range(0, 10, 1)
    print dir(list)
    x = 2
    print eval('x+3')
    print chr(97), ord('a')
    print divmod(11, 3)

def demo_controlflow():
    score = 65
    if score > 99:
        print 'a'
    elif score > 60:
        print 'b'
    else:
        print 'c'
    while score < 100:
        print score
        score += 10

    for i in range(0, 10, 2):
        if i == 0:
            pass
        if i < 5:
            continue
        print i
        if i == 6:
            break;

def demo_list():
    lista = [1, 2, 3]
    print lista
    listb = ['a',1,'a']
    print listb
    lista.extend(listb)
    print lista
    print len(lista)
    print 'a' in listb
    listb.insert(0,'hah')
    print listb
    listb.pop(1)
    print listb
    listb.reverse()
    print listb
    print listb[0]
    listb.sort()
    print listb * 2

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def demo_dictionary():
    dicta = {1: 1, 2: 4, 3: 9}
    print dicta
    print dicta.keys(), dicta.values()
    print dicta.has_key(1), dicta.has_key('3')
    for key, value in dicta.items():
        print key, value
    dictb = {'+': add, '-': sub}
    print dictb['+'](1, 2)
    print dictb.get('-')(15, 3)
    dictb['*'] = 'x'
    print dictb
    dicta.pop(1)
    print dicta
    del dicta[2]
    print dicta

def demo_set():
    seta = set((1, 2, 3))
    setb = set((2, 3, 4))
    print seta
    seta.add(4)
    print seta
    print seta & setb, seta.intersection(setb)
    print seta | setb, seta.union(setb)
    print seta - setb
    print len(seta)

if __name__ == '__main__':

    # print 'hello newcoder '
    # demo_string()
    # demo_controlflow()
    # demo_list()
    # demo_dictionary()
    demo_set()
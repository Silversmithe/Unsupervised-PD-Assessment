# OBJECT START
class Result(object):

    # constructor - initializes the object
    def __init__(self):
        self._val1 = 2

    # class function
    def function1(self,a,b,c):
        d=a+b+c+self._val1
        return d

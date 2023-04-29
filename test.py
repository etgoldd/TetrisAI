
class testclass:

    def __init__(self, value):
        self.a = value

initfunc = testclass.__init__

obj= initfunc(12)

print(type(obj))
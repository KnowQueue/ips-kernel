
def constructor(cls, *prototype):
    working_mem = cls.working_mem
    instance_key = cls.__name__
    for letter in prototype:
        instance_key += "_{:s}".format(letter)
    if instance_key in working_mem["instances"]:
        return working_mem["instances"][instance_key]
    else:
        inner_class_name = cls.__name__[:(len(cls.__name__)-len("_Mixin"))]
        inner_class = getattr(cls, inner_class_name)
        working_mem["instances"][instance_key] = inner_class(prototype)
        return working_mem["instances"][instance_key]

def initializer(self, prototype):
    print(prototype)

string = """
a = TRIANGLE("A","B","C")
b = TRIANGLE("A","B","C")
c = TRIANGLE("A","B","F")
"""

def session(string):
    working_mem = {
        "instances": {}
    }

    locals()["TRIANGLE"] = type("TRIANGLE_Mixin",(object,),{
        "TRIANGLE": type("TRIANGLE",(object,), {
            "__init__": initializer
        }),
        "working_mem": working_mem,
        "__new__": constructor,
    })

    exec(string, globals(), locals())

session(string)
session(string)



instances = {}

def constructor(cls, *prototype):
    instance_key = cls.__name__
    for letter in prototype:
        instance_key += "_{:s}".format(letter)
    if instance_key in instances:
        return instances[instance_key]
    else:
        inner_class_name = cls.__name__[:(len(cls.__name__)-len("_Mixin"))]
        inner_class = getattr(cls, inner_class_name)
        instances[instance_key] = inner_class()
        return instances[instance_key]

def initializer(self):
    print("Created a new object")

globals()["TRIANGLE"] = type("TRIANGLE_Mixin",(object,),{
    "TRIANGLE": type("TRIANGLE",(object,), {
        "__init__": initializer
    }),
    "__new__": constructor,
})

string = """
a = TRIANGLE("A","B","C")
print(a)
b = TRIANGLE("A","B","C")
print(b)
c = TRIANGLE("A","B","F")
print(c)
"""

exec(string)


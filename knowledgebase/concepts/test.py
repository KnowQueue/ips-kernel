
def constructor(self, *prototype):
    instance_key = self.__class__.__name__
    for letter in prototype:
        instance_key += "_{:s}".format(letter)
    if instance_key in self.__class__.instances:
        return self.__class__.instances[instance_key]
    else:
        self.__class__.instances[instance_key] = self

globals()["TRIANGLE"] = type("TRIANGLE",(object,),{
    "instances": {},
    "__init__": constructor,
})


a = TRIANGLE("A","B","C")
print(a)

b = TRIANGLE("A","B","C")
print(b)
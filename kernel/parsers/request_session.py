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

def request_session(requestBody, kernel_globals):
    working_mem = {
        "instances": {}
    }

    for concept in kernel_globals["concepts"]:
        data = concept.model
        locals()[data['name']] = type(data['name']+"_Mixin",(object,),{
            data['name']: kernel_globals["concepts"][data['name']],
            "working_mem": working_mem,
            "__new__": constructor,
        })

    result = exec(requestBody, globals(), locals())
    print(globals().keys())

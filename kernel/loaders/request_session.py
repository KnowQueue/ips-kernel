
import sys
from io import StringIO
import contextlib
import traceback
from kernel.functions.list_all import list_all

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def constructor(cls, *prototype):
    working_mem = cls.working_mem
    instance_key = cls.__name__[:(len(cls.__name__)-len("_Mixin"))]
    for letter in prototype:
        instance_key += "_{:s}".format(letter)
    if instance_key in working_mem["instances"]:
        return working_mem["instances"][instance_key]
    else:
        inner_class_name = cls.__name__[:(len(cls.__name__)-len("_Mixin"))]
        inner_class = getattr(cls, inner_class_name)
        working_mem["instances"][instance_key] = inner_class(prototype, working_mem)
        return working_mem["instances"][instance_key]

def create_function(func, global_mem, local_mem, working_mem):
    def function_template(*args, **kwargs):
        return func(global_mem, local_mem, working_mem, *args, **kwargs)
    return function_template

def request_session(requestBody, kernel_globals):
    working_mem = {
        "constructors": {},
        "instances": {}
    }

    for concept in kernel_globals["concepts"]:
        data = kernel_globals["concepts"][concept].model
        locals()[data['name']] = type(data['name']+"_Mixin",(object,),{
            data['name']: kernel_globals["concepts"][data['name']],
            "working_mem": working_mem,
            "__new__": constructor,
        })
        working_mem["constructors"][data['name']] = locals()[data['name']]
    
    locals()["list_all"] = create_function(list_all, kernel_globals, locals(), working_mem)
    
    with stdoutIO() as s:
        try:
            exec(requestBody, globals(), locals())
        except SyntaxError as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            print("%s at line %d: %s" % (error_class, line_number, detail))
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            tb_in_requestBody = [trace for trace in traceback.extract_tb(tb) if trace[0] == "<string>"]
            # print(detail)
            # print(traceback.extract_tb(tb))
            # print(tb_in_requestBody)
            line_number = tb_in_requestBody[0][1]
            print("%s at line %d: %s" % (error_class, line_number, detail))
    return s.getvalue()

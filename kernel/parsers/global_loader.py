def initializer(self, prototype):
    print(prototype)

def global_loader(kernel_globals):
    kernel_globals["TRIANGLE"] = type("TRIANGLE",(object,), {
        "__init__": initializer
    })
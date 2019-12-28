import os
from settings import APP_KB
import json

def initializer(self, prototype):
    print(prototype)

def global_loader(kernel_globals=None):
    conceptsPath = os.path.join(APP_KB, "concepts")
    concepts = os.listdir(conceptsPath)

    for conceptFile in concepts:
        with open(os.path.join(conceptsPath, conceptFile)) as json_file:
            data = json.load(json_file)
            obj = {
                "model": data,
                "__init__": initializer
            }
            kernel_globals["concepts"][data['name']] = type(data['name'],(object,), obj)
# class TRIANGLE:
#     def __init__(self, prototype):
#         pass
    
    

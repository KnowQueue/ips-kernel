import os
from settings import APP_KB
import json

def initializer(self, identifier, working_mem):
    constructors = working_mem["constructors"]
    model = self.__class__.model
    if not (len(identifier) == len(model["prototype"])):
        raise KeyError("{:s} must have {:d} identifiers.".format(self.__class__.__name__,len(model["prototype"])))
    prototypeIdentifierMap = {}
    for index, letter in enumerate(model["prototype"]):
        prototypeIdentifierMap[letter] = identifier[index]
    self.__identifier__ = identifier
    self.__attr__ = {}
    for attr in model["attributes"]: 
        meta = model["attributes"][attr]
        attName = attr
        attConcept = meta["type"]
        attPrototype = [] if "prototype" not in meta else meta["prototype"]
        attIdentifier = [prototypeIdentifierMap[letter] for letter in attPrototype]
        if attConcept in constructors:
            self.__attr__[attName] = constructors[attConcept](*attIdentifier)
        else:
            self.__attr__[attName] = None

def to_string(self):
    return "{:s}{:s}".format(self.__class__.__name__, str(self.__identifier__))

def global_loader(kernel_globals=None):
    conceptsPath = os.path.join(APP_KB, "concepts")
    concepts = os.listdir(conceptsPath)

    for conceptFile in concepts:
        with open(os.path.join(conceptsPath, conceptFile)) as json_file:
            data = json.load(json_file)
            class_attrs = {
                "model": data,
                "__init__": initializer,
                "__str__": to_string,
            }
            kernel_globals["concepts"][data['name']] = type(data['name'],(object,), class_attrs)
# class TRIANGLE:
#     def __init__(self, prototype):
#         pass
    
    

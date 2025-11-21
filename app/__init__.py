# @description: 
# @author: licanglong
# @date: 2025/11/20 11:40
import importlib
import pkgutil

from app import handler

for finder, name, ispkg in pkgutil.iter_modules(handler.__path__, handler.__name__ + "."):
    importlib.import_module(name)

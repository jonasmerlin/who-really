import os
import glob
import importlib

# find module names in the directory
dirs = glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/*")
module_names = [os.path.basename(m) for m in dirs if os.path.basename(m) != "__init__.py" and os.path.basename(m) != "__pycache__"]
# import every module using importlib

modules = [importlib.import_module('classifiers.' + m + '.predict') for m in module_names]
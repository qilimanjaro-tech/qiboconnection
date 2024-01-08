import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils"))

if utils_path not in sys.path:
    sys.path.insert(0, utils_path)

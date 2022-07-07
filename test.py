from importlib.resources import path
import os

path=os.getcwd()

# print(path)
file_path="static/media"


l=os.path.join(path,file_path)

print(l,'***********')
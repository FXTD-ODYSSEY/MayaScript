import os
import configparser

path = r"F:\nodeline\adam_pose_editor\.gitmodules"
print(open(path).read())

config = configparser.ConfigParser()
config.read(path)

for value in config.values():
    path = value.get("path")
    print(path)


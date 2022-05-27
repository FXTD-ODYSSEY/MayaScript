import os

DIR = os.path.dirname(os.path.realpath(__file__))
for f_path in os.listdir(DIR):
    print(f_path)
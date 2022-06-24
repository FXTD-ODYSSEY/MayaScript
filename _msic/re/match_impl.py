# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"_impl(\[\D*?\])*?_"
print(regex.replace("_","_@",1))
test_str = ("main_window_impl_file_menu\n"
	"main_window_impl[maya]_file_menu")

matches = re.search(regex, test_str, re.MULTILINE)
print(matches)

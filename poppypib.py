# This script is to truncate the pypi badge upon deploying to reduce redundancy
# poppypib - Pop PyPi Badge

import re

def edit_file(file: str, value: str='', regex=None):
   with open(file, 'r+') as f:
      text = f.read()
      f.seek(0)
      if value != '' and regex == None:
         new_text = re.sub(fr"{value}", '', text)
      else:
         new_text = re.sub(expr, '', text)
      f.write(new_text)
      f.truncate()

expr = re.compile(r"<a.+pypi.+\n.+\n</a>\n\n")
edit_file("README.md", regex=expr)

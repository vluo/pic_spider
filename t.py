import os, glob
from urllib.parse import urlparse


o = urlparse('http://www.cwi.nl/%7Eguido/Python.html')

print(o[1])

import os, glob



file = os.getcwd()+'/*.py'
r = glob.glob(r'*.py')
print(file)
if r is None or len(r)==0:
    print('no')
else:
    print(r)

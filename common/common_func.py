import os, sys


def add_log(file, line, mode='w+'):
    path = os.path.dirname(file)
    if not os.path.exists(path):
        os.makedirs(path)
    #end if
    try:
        with open(file, mode, encoding='utf-8') as file:
                file.write(str(line))
                return True
        # end with
    except IOError:
        return False
#end def
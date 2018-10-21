from ctypes import *
import os

if __name__ == "__main__":
    clib = cdll.LoadLibrary('/Users/devsh/PycharmProjects/gif-resize/lib')
    #print 'clib.time() = %d' % clib.time(None)
    #clib.printf("clib.printf(s) = <%s>\n", s)

    mylib = cdll.LoadLibrary('%s/libmylib.so' % os.getcwd())
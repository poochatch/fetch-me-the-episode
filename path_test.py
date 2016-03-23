import os, sys
from subprocess import call


print 'call("pwd")'
call('pwd')
print 'call("ls")' 
call('ls')
print 'sys.argv[0]', sys.argv[0]
print 'os.getcwd()', os.getcwd()
print 'os.path.abspath("")', os.path.abspath('')
print 'os.path.dirname(sys.argv[0])'
os.path.dirname(sys.argv[0])
print 'os.path.abspath(os.path.dirname(sys.argv[0]))', os.path.abspath(os.path.dirname(sys.argv[0]))
print ''

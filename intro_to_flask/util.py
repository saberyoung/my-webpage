import socket
import sys

host = socket.gethostname()
if host in ['dark']:
   host = 'dark'
   workingdirectory = '/dark/hal/dlt40/'
   execdirectory = '/dark/hal/bin/'
   rawdata = '/archive/engineering/'
   realpass = 'configure'
elif 'physics.ucdavis' in host:
   host = 'laptop'
   workingdirectory = '/Users/valenti/data/dlt40/'
   execdirectory = '/Users/valenti/bin/'
   rawdata = '/archive/engineering/'
   realpass = 'configure'
elif 'ucdavis.edu' in host or host in ['pluto.local','airbears2-10-142-137-9.airbears2.1918.berkeley.edu','localhost:8080']:
   host = 'syang'
   workingdirectory = '/'
   execdirectory = '/'
   rawdata = '/'
   realpass = 'configure'
else:
   sys.exit('system '+str(host)+' not recognize')

####################################################
def readpasswd(directory,_file):
    from numpy import genfromtxt
    data=genfromtxt(directory+_file,str)
    gg={}
    for i in data:
        try:
            gg[i[0]]=eval(i[1])
        except:
            gg[i[0]]=i[1]
    return gg

readpass = readpasswd(workingdirectory,realpass)
#print readpass

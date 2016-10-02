#!/usr/bin/python2
import re
import subprocess
import os

p = subprocess.Popen(["svnversion","/home/pablo/reactos-work/trunk/reactos"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
p.wait()
m = re.match(r'(|\d+M?S?):?(\d+)(M?)S?', p.stdout.read())
rev = int(m.group(2))
new_name="bootcd-mine-"+str(rev)+".iso"
print new_name
os.rename("/home/pablo/reactos-work/rosbuild/reactos/bootcd.iso","/home/pablo/reactos-work/"+new_name)       


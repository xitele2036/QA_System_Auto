# -*- coding: utf-8 -*-

import os
import subprocess
cmd = 'VG859LAN-argv.exe 10.86.40.199 -timing935 '
p = os.popen(cmd)
#sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr = subprocess.STDOUT)
sub = subprocess.Popen(cmd,shell=True)
pattern = 'VG859LAN-argv.exe 10.86.40.199 -pat911'
print("patterN:",pattern)
#pat = subprocess.Popen(pattern,shell=True)
subprocess.Popen('VG859LAN-argv.exe 10.86.40.199 -pat911',shell=True)






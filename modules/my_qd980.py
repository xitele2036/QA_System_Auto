
# -*- coding: utf-8 -*- 
import telnetlib
import time
from modules.TestCfgParse import TestCfgParse

class Telnet_QD980(object):
    def _init_(self):
        pass
    
        
    def do_telnet(self,timing,pattern,signaltype,samplemode,bitdepth): 
        
        #Read the QD980 configuration
        
        QD980Cfg = TestCfgParse()
        hostIP = QD980Cfg.GetTestCfgInfo('QD980_IP') #Telnet Server IP
        print("QD980 IP address:", hostIP)
        username=QD980Cfg.GetTestCfgInfo('QD980_UserName') # username
        print("QD980 Username:", username)
        password=QD980Cfg.GetTestCfgInfo('QD980_PW') # password
        print("QD980 Password:", password)

        finish = 'producer-nhdmi2>'  # command prompt

        # '''Telnet log in：Windows client connects Linux server'''
      
      
        try:
            # Connect Telnet Server
            tn = telnetlib.Telnet(hostIP.encode('utf-8'))
            print('%s Connected Successfully!'%hostIP)
            
        except:
            print('%s Connection Failure, please check networtwok configuration.'%hostIP)
            return False
        
        # Input login username
        tn.read_until(b'login: ',timeout=10)
        tn.write(username.encode('ascii') + b"\n")
        print("username entered")

        # Input login password
        tn.read_until(b'Password: ',timeout=10)
        tn.write(password.encode('ascii') + b"\n")
        print("password entered")
        
        loginResult = tn.read_very_eager().decode('utf-8')
        print(loginResult)
        if 'Login Incorrect' not in loginResult:
            print('%s Login Successfully'%hostIP)
        else:
            print('%s Login Failure'%hostIP)


        # Input 4 to enter HDMI module
        tn.read_until(b'#p2-scope>')
        tn.write('5'.encode('ascii') + b"\n")       #different QD980 has different slot
        print("slot is 1")
        
        # Input command and pattern，then stop Telnet connection
        
        tn.read_until(finish.encode())
        print("finish is",finish)
        tn.write(timing.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(pattern.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(signaltype.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(samplemode.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(bitdepth.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write('ALLU'.encode('ascii') + b"\n")
        time.sleep(1)
        tn.close() # tn.write('exit\n')


if __name__=='__main__':
    Telnet_QD980_Pattern = Telnet_QD980()
    Telnet_QD980_Pattern.do_telnet('FMTL 1080p60','IMGL GrayBar','DVST 10','','NBPC 10' )
    time.sleep(10)
    Telnet_QD980_Pattern.do_telnet('FMTL 1080p60','IMGL ColorBar','DVST 10','','NBPC 10' )

 


 

 


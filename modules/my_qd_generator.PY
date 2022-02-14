# -*- coding: utf-8 -*-

import threading
from my_serial import SigmaSerial
from TestCfgParse import TestCfgParse

class DEV_QD_GEN(object):
    def QD_Write(self,command):

        #Read the QD device COM configuration
                
        QDCfg = TestCfgParse()
        dev_qd_port = QDCfg.GetTestCfgInfo('DEV_QD_PORT') #QD device COM port
        print("QD Device Serial Configuration:", dev_qd_port)
             
                
        if command is None:
            return False
        else:
            self.QD_Serial=SigmaSerial()
            
            try:
                # Connect with COM port
                self.QD_Serial.open(dev_qd_port)
                print('%s Connected Successfully!'%dev_qd_port)
                
            except:
                print('%s Connection Failure, please check serial port configuration.'%dev_qd_port)
                return False            
            
            self.QD_Serial.write(command)
            print(command)
            self.QD_Serial.write('ALLU' + '\n')
            self.QD_Serial.close

if __name__ == '__main__':
    QD_Pattern_Gen=DEV_QD_GEN()
    QD_Pattern_Gen.QD_Write('logcat')

                
        
     

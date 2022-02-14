# -*- coding: utf-8 -*-

#
# Simple Python test program to use the RedRatHub.
#
# Ethan Johnson, David Blight, Chris Dodge - RedRat Ltd.
#


import modules.RedRatHub
import time
AutoTestAppINI = './Config/AutoTestApp.INI'


class DEV_REDRAT(object):
    def IR_GEN(self,IRMessage,PauseTimer):
        
        cfgList = ''
       
        try:            
            with open(AutoTestAppINI, 'r') as f:
                cfgList = [line.strip() for line in f.readlines()]
                #print cfgList
                f.close()
        except:
            pass
        
        for item in cfgList:
            if item.startswith('TestPC_IP'):
                test_pc_ip=item.split("=")[1]
               
            elif item.startswith('RedRat_Name'):
                redRat_Name=item.split("=")[1]
                
            elif item.startswith('RedRat_dataset'):
                redRatDataset=item.split("=")[1]
                
        print('You are using %s redrat and %s.xml dataset on %s test PC!'%(redRat_Name,redRatDataset,test_pc_ip))
        
        client = RedRatHub.Client()
        
        # Connect to the RedRatHub
        client.OpenSocket(test_pc_ip, 40000)

        # Send some IR signals

        client.SendMessage('name="'+redRat_Name+'" dataset="'+redRatDataset+'" signal="'+IRMessage+'" output="12:10"')
        print("Sent signal*\n")
        time.sleep(PauseTimer)



        # List the datasets known by the hub
        print("List of datasets:")
        list = client.ReadData('hubquery="list datasets"')
        print(list)

        client.CloseSocket()
        print("Finished.")

if __name__ == '__main__':
    RedRat=DEV_REDRAT()
    RedRat.IR_GEN('menu',2)

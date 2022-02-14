import subprocess
from subprocess import *
import os
import time

class AliSteamerPlayer(object):
    
    def isRunning(self,processName):
        try:
            print(('tasklist | findstr '+processName))
            process=len(os.popen('tasklist | findstr '+processName).readlines())
            print(process)
            
            if process >=1:
                return True
            else:
                return False
        except:
            print('Programe error')
            return False

        
    def Ali_DTV_Player(self,streamName,freq,loopTimes):    
            
        # ATPlayRec args definition
        
        args = [
            ['--play', streamName],
            ['--frequency', freq],      
            ['--loop', loopTimes],
            ['-v',4]
    
        ]
    
        aliPlayCmd = 'ATPlayRec.exe '
        for arg in args:
            aliPlayCmd += '{} {} '.format(arg[0], arg[1])
        print(aliPlayCmd)
        
        aliStatus=self.isRunning('ATPlayRec.exe') 
        print(aliStatus)
        
        if aliStatus==True:
            stopATProcess=os.popen('taskkill /F /IM ATPlayRec.exe')
            time.sleep(10)
            print("The running ATPlayRec Progrom was stopped!")
            
        print("Start Alitronic Player...")
        
        aliPlayer_proc=subprocess.Popen(aliPlayCmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
      
        '''
        cmdInfo=''
        print "Starting"
        for line in iter(aliPlayer_proc.stdout.readline,b''):
            print line.strip()
            if "Playing file....." in line.strip():
                cmdInfo = line
                print cmdInfo
                print "The stream in case is playing..."
                
            if "Playing file Done" in line.strip():
                print "Stream playback was finished"
                
            if not subprocess.Popen.poll(aliPlayer_proc) is None:
                if line =="":
                    break
        
        aliPlayer_proc.stdout.close()
        '''

if __name__ == "__main__":
    
    DTVStreamPlayback=AliSteamerPlayer()
    DTVStreamPlayback.Ali_DTV_Player('1080I.trp',183.0,1)
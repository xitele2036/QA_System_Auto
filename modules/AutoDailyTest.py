# -*- coding: utf-8 -*-

import sys
import os
#import struct
import time
import pandas as pd
import subprocess

#import copy

import threading
from modules.my_serial import SigmaSerial

from modules.my_imghash import ImageMatch

from modules.ReSTTerminal import restterminal
from modules.MyOTTCast import Tablet_Cast_Test
from modules.My_RestKey import Restkey_define

from modules.MyRedRat import DEV_REDRAT
from modules.XML_Parsedata import XML_PARSE
from modules.my_net_controller import netIRControl

from modules.MyCamera import CameraCapture
from modules.my_qd980 import Telnet_QD980
from MyFFmpegRecorder import FFMpegCapture
from modules.MyReFiler import ReFilter
from modules.my_epcr3 import PowerController
from modules.MyAliStreamer import AliSteamerPlayer
Auth_Token = "./Config/Auth_Token.txt"
AutoTestAppINI = './Config/AutoTestApp.INI'

class AutoDailyTest(object):
    
  def GetTestCfgInfo(self,cfgItem):
      cfgList = ''
      try:            
          with open(AutoTestAppINI, 'r') as f:
              cfgList = [line.strip() for line in f.readlines()]
              #self.fileList                
              f.close()
      except:
          pass  
      #self.AutoTestInfoFile = 'Sanity_Test.xlsx'
      for item in cfgList:
          if item.startswith(cfgItem):
              return item.split("=")[1] 
        
             
  def ReadAutoTestInfo(self, filename='Sanity_Test.xlsx'):

    # read Source Sheet to get the source list firstly
    self.case = pd.read_excel(filename, 'Test_Cases', index_col=None)
    #return case

    
    
        
  def serial_start(self,portname,dut_logfileName):
    
        
    if self.dut_serial is None:
        self.dut_serial = SigmaSerial()    
            
    try: 
      
      self.dut_serial.open(portname)
      
                     
      if self.dut_serial.isOpen():
          #self.waitEnd = threading.Event()
          self.alive = True
          self.thread_read = threading.Thread(target=self.serial_reader,args=(dut_logfileName,))
          self.thread_read.setDaemon(True)
          self.thread_read.start()      
          return True
          
      else:
          print('Serial has not been started\n')
          return False
      
    except Exception as ex:
        print (ex)
        return False
     
        
  def serial_reader(self,dut_logfileName):
    
        
    while self.alive:
           
      try:
                         
        t = time.localtime(time.time())
        strLogtime=time.strftime("[%Y-%m-%d-%H:%M:%S]", t)          
        data = self.dut_serial.readline().decode('utf-8') 
        #print "data length:%s"%len(data)
                 
        if len(data) > 1 and self.dut_serial.isOpen():
            #data.AppendText(data.strip()+'\n')
            data = strLogtime + self.dut_serial.readline().decode('utf-8') 
            logfile=open(dut_logfileName,'a')
            logfile.write(data)
            logfile.close() 
        '''    
        else:
          data = "\n---The End---\n"
          logfile=open(dut_logfileName,'a')
          logfile.write(data)
          logfile.close()   
        '''

      except Exception as ex:
          print (ex)

    #self.waitEnd.set()
    self.alive = False

  def serial_stop(self):
    #self.thread_read.join()
    if not self.dut_serial is None:
      self.alive = False
      if self.dut_serial.isOpen():
        self.dut_serial.close()
          
  def qd_serial_start(self,qd_portname):

    if self.qd_serial is None:
      self.qd_serial = SigmaSerial()
  
    try:
      self.qd_serial.open(qd_portname)

      if self.qd_serial.isOpen():
        #self.waitEnd = threading.Event()
        self.alive = True

        self.thread_read = threading.Thread(target=self.qd_serial_reader)
        self.thread_read.setDaemon(True)
        self.thread_read.start()
        return True
      else:
        print("QD Serial has not been started\n")
        return False
    except Exception as ex:
      print (ex)
      return False

  def qd_serial_reader(self):
    while self.alive:
      try:

        data = self.qd_serial.readline().decode('utf-8') 
        if len(data) > 1:
          self.serialmsg.AppendText(data.strip()+'\n') 
          
      except Exception as ex:
        print (ex)

    #self.waitEnd.set()
    self.alive = False


  def qd_serial_stop(self):
    #self.thread_read.join()
    if not self.qd_serial is None:
      self.alive = False
      if self.qd_serial.isOpen():
        self.qd_serial.close() 
  
  def SaveResult(self,filename,caseData):

    #df=pd.DataFrame(self.case)
    df=pd.DataFrame(caseData)
    writer=pd.ExcelWriter(filename)
    df.to_excel(writer,'Test_Cases',index = False)
    writer.save()
    writer.close()  
    
  def mkdir(self,path):
    
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    
    if not isExists:
      os.makedirs(path)
      print("%s is created successfuly!"%path)
      return True
    else:
      print("%s has existed!"%path)
      return False
    
       
  def RunCase(self,filename): 
           
    #Load test case file
    print('test file is:',filename)
    try:                       
      self.case = pd.read_excel(filename, 'Test_Cases', index_col=None)
    except:
      print("ERROR: handle file %s"%filename)
   
    #Make folder named by build number in .\Video folder to save recorded pic and video
    videoPath=".\\Video\\#"+gpus+"\\"
    #print videoPath
    self.mkdir(videoPath)
     
    
    # DUT port connection, capture one log file for all cases
    #self.dut_serial = None
    #board_port= self.GetTestCfgInfo('Board_PORT')
    #print 'DUT Board Port:',board_port
    #logFN='.\\Logs\\DUT_Log_#'+gpus+'.txt'
    #print "%s logfile will be created"%logFN
    #self.serial_start(board_port,logFN)
    
    
    #QD780 UART Port Connection
    self.qd_serial = None 
    dev_qd_port= self.GetTestCfgInfo('DEV_QD_PORT')
    print("QutumData QD780 COM PORT:",dev_qd_port)
    if dev_qd_port!='':
      self.qd_serial_start(dev_qd_port)
    else:
      print('Please Configure Correct COM Port if need use QD780 during test!')
    
    #Camera Connection, initialize camera for AV record with FFMPEG
    CameraVDN=self.GetTestCfgInfo("Camera_Video_Device_Name")
    CameraADN=self.GetTestCfgInfo("Camera_Audio_Device_Name") 
    ffmpegCap=FFMpegCapture()
    ffmpegCap.cameraInit(CameraVDN)    
        
        
    # Run test Case
    #Get the local time
    t = time.localtime(time.time())
    strIMStime=time.strftime("-%Y-%m-%d-%H-%M-%S", t)
    
    #Get the total case number
    i=0
    retryTimes=0
    caseNum=self.case.iloc[:,0].size
    print("%s test cases will be exectuted and test start"%caseNum)
    
    while i<caseNum:
      
      print("*****TEST CASE %s/%s IS RUNNING*****"%((i+1),caseNum))  
      
      # DUT port connection
      self.dut_serial = None
      board_port= self.GetTestCfgInfo('Board_PORT')
      print('DUT Board Port:',board_port)
      
      logFN='.\\Logs\\DUT_Log_#'+gpus+'_'+self.case.loc[i]['Test_Case_ID']+'.txt'
      print("%s logfile will be created"%logFN)
      self.serial_start(board_port,logFN)      
    
      # Camera Thread Creation
      if str(self.case.loc[i]['PIC_Capture'])!='nan':
        capFileName =''
        capTime=0             
        #cap = CameraCapture()
          
        # get the capture file name
        capFileName = self.case.loc[i]['PIC_Capture'].strip().split(']')[1].split(',')[0]
        capTime = self.case.loc[i]['PIC_Capture'].strip().split(']')[1].split(',')[1]
        capDir=videoPath+capFileName
        print('%s is captured!'%capDir)
        print('capture time is',capTime)
        
        #Capture video with Opencv lib
        #self.thread_camera=threading.Thread(target=cap.videoCapture,args=(capDir+strIMStime,capTime))
        
        #Capture AV with FFMPEG
        self.thread_camera=threading.Thread(target=ffmpegCap.ffmpeg_video_record,args=(CameraVDN,CameraADN,capDir+strIMStime+'.mkv',capTime,'"'+self.case.loc[i]['Test_Case_ID'].strip()+' '+self.case.loc[i]['Case_Description'].strip()+'"'))
        
        if 'CAM-VIDEO-START' in self.case.loc[i]['PIC_Capture'].strip():
            print('***********************The video is in recording**************************')
            # open the camera
            #cap.open()  
            self.thread_camera.setDaemon(True)
            self.thread_camera.start() 
            #print 'the record is finished'
       
        else:
            print('***********************No Video record is required*************************')        
      
      # Rest/Cast Control Start
      #math.isnan(self.case.loc[i]['Rest_Control'])

      if str(self.case.loc[i]['Rest_Control'])!='nan':
          
          print("Current Function:",self.case.loc[i]['Rest_Control'].strip().split(']')[0].split('[')[1])
          
          if self.case.loc[i]['Rest_Control'].strip().split(']')[0].split('[')[1]=='REST':
              rest = restterminal()
              restCommand=self.case.loc[i]['Rest_Control'].strip().split(']')[1]
              print('RESTCommand:',restCommand)
      
              if restCommand=="PAIR":
                  self.auth_token = rest.pair()
                  fw=open(Auth_Token, "w")
                  fw.write(self.auth_token)
                  fw.close()
              
              else:
                  fr=open(Auth_Token, "r")
                  self.read_auth_token=fr.readline().strip('\n')
                  fr.close()
               
                  rest.read_dictionary()                             
                  #requests.packages.urllib3.disable_warnings()
                  restValue=rest.parse_command(restCommand,self.read_auth_token)
                  print('restValue:',restValue)
                  time.sleep(3)
                  #Write restlog into file
                  #rest.parse_command("restlog",self.read_auth_token)
          elif self.case.loc[i]['Rest_Control'].strip().split(']')[0].split('[')[1]=='CAST':
                              
              OTTCast = Tablet_Cast_Test()
             
              #Parse OTT name, movie name and playback time.
              castCommand=self.case.loc[i]['Rest_Control'].strip().split(']')[1]
              OTTName=castCommand.strip().split(',')[0]
              MovieName=castCommand.strip().split(',')[1]
              PlayBackTime=castCommand.strip().split(',')[2]
              
              print('CAST',OTTName)
              print('MovieName',MovieName)
              print('PlayBackTime',PlayBackTime)
              
              if OTTName=='Netflix':
                  OTTCast.Cast_Netflix(OTTName,MovieName,PlayBackTime)
                  
              elif OTTName=='YouTube':
                  OTTCast.Cast_Youtube(OTTName,MovieName,PlayBackTime)
                  print('Youtube movie:',MovieName)
              elif OTTName=='PlayMusic':
                OTTCast.Cast_PlayMusic(OTTName,MovieName,PlayBackTime)
                print('PlayMusic:',MovieName)
              elif OTTName=='Disney+':
                OTTCast.Cast_DisneyPlus(OTTName,MovieName,PlayBackTime)
                print('DisneyPlus:',MovieName)
              elif OTTName=='Hulu':
                  OTTCast.Cast_Hulu(OTTName,MovieName,PlayBackTime)
                  print('Hulu movie:',MovieName)
          elif self.case.loc[i]['Rest_Control'].strip().split(']')[0].split('[')[1]=='REMOTEKEY':
              restKey=Restkey_define()
              restKeyCommand=self.case.loc[i]['Rest_Control'].strip().split(']')[1]
              print('Rest Key Commands:%s'%restKeyCommand)
              
              if ":" in restKeyCommand:
                  print('Execute Remote key list from file:%s'%restKeyCommand)
                  #restKeyCaseFolder=restKeyCommand.strip().split[0]
                  #restKeyCaseName=restKeyCommand.strip().split[1]
                  #restKey.Rest_GroupKeys_Play("%s\%s"%(restKeyCaseFolder,restKeyCaseName))
                  restKey.Rest_GroupKeys_Play(restKeyCommand)
              else:
                  restKeyCommand_index=0
                  restKeyCommand_List=restKeyCommand.strip().split(',')
                  while restKeyCommand_index < len(restKeyCommand_List):
                      restKeyCommand_Message=restKeyCommand_List[restKeyCommand_index]
                      restKeyCommand_PauseTimer=float(restKeyCommand_List[restKeyCommand_index+1])
                      restKey.Rest_SingleKey_Play(restKeyCommand_Message,restKeyCommand_PauseTimer)
                      restKeyCommand_index=restKeyCommand_index +2                       
                                                    
          else: 
              print('%s function not support!'%(case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]))
      else:
          print('Rest Case is null')
                               
      #RedRat Control Start
      
      if str(self.case.loc[i]['IR_Seq'])!='nan':
          IR_Commands = self.case.loc[i]['IR_Seq'].strip().split(']')[1]
          print("NetRat IR Commands :",IR_Commands)
                      
          if "RedRat" in self.case.loc[i]['IR_Seq'].strip():
              
              RedRat=DEV_REDRAT()
              if '.xml' in IR_Commands:
                  print("run xml parser")
                  Xml_data=XML_PARSE()
                  IR_Macro= Xml_data.Parameter(IR_Commands.strip().split(':')[0],IR_Commands.strip().split(':')[1])
                  print("IR sequence:",IR_Macro)
                  IR_index=0
                  while IR_index < len(IR_Macro):
                      RedRat.IR_GEN(IR_Macro[IR_index],IR_Macro[IR_index+1])
                      IR_index= IR_index +2
                  
              else:
                  IR_index=0
                  IR_List=IR_Commands.strip().split(',')
                  while IR_index < len(IR_List):
                      RedRat_Message=IR_List[IR_index]
                      RedRat_PauseTimer=float(IR_List[IR_index+1])
                      RedRat.IR_GEN(RedRat_Message,RedRat_PauseTimer)
                      IR_index=IR_index +2
          elif "NetRat" in self.case.loc[i]['IR_Seq'].strip():
              print('Send keys by NetRat!')
              NetRat_Control=netIRControl()
              
              if ":" in IR_Commands:
                  
                  print('Read the IR key sequence for file in testsuite')
                  NetRat_CaseFolder=IR_Commands.strip().split(':')[0]
                  NetRat_CaseName=IR_Commands.strip().split(':')[1]
                  print('Case Folder:',NetRat_CaseFolder)
                  print('Case Name:',NetRat_CaseName)
                  NetRat_Control.autoplaycase(NetRat_CaseFolder,NetRat_CaseName)
              else:
                  NetRatIR_index=0
                  NetRatIR_List=IR_Commands.strip().split(',')
                  while NetRatIR_index < len(NetRatIR_List):
                      NetRat_Message=NetRatIR_List[NetRatIR_index]
                      NetRat_PauseTimer=float(NetRatIR_List[NetRatIR_index+1])
                      NetRat_Control.say_playsinglekey(NetRat_Message,NetRat_PauseTimer)
                      NetRatIR_index=NetRatIR_index +2                    
                   
                   
       
      #DUT Serial Control
      
      if str(self.case.loc[i]['SerialCmd'])!='nan':
          
          ser_cmd_list = self.case.loc[i]['SerialCmd'].strip().split(';')
  
          ser_cmd_index = 0
          print(len(ser_cmd_list))
          while ser_cmd_index < len(ser_cmd_list):
              print('Execute the serial command:',ser_cmd_list[ser_cmd_index])
              self.dut_serial.write(ser_cmd_list[ser_cmd_index].encode('utf-8'))
              time.sleep(float(ser_cmd_list[ser_cmd_index+1]))
              ser_cmd_index = ser_cmd_index+2
      
          
      # Pattern Generator Control 
      # Quantum Data 780, 980 and AstroVG859 could be controled by typical word "VG859","QD780" and "QD980" in test case
      

      if str(self.case.loc[i]['Device_Control'])!='nan':
          devCommand=self.case.loc[i]['Device_Control'].strip().split(']')[1]
          print("The device command for QD, Astro, EPCR3 or Alitronika Streamer:",devCommand)
          
          if 'VG859' in self.case.loc[i]['Device_Control'].strip():
            VG859_ip= self.GetTestCfgInfo('VG859_IP')
            print("VG859 IP address:",VG859_ip)
                          
            vg859_timing=devCommand.split(',')[0]
            vg859_pattern=devCommand.split(',')[1]
            print("VG859 timing and pattern",vg859_timing,vg859_pattern)
            print('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_timing)
            print('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_pattern)
            
            subprocess.Popen( '.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_timing,shell=True)
            subprocess.Popen( '.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_pattern,shell=True)
            time.sleep(3)
                      
          elif 'QD780' in self.case.loc[i]['Device_Control'].strip():    
              qd780_timing = devCommand.split(',')[0]
              qd780_pattern = devCommand.split(',')[1]
    
              self.qd_serial.write(qd780_timing.encode('utf-8'))
              self.qd_serial.write(qd780_pattern.encode('utf-8'))
              self.qd_serial.write('ALLU' + '\n')
              time.sleep(3)
              print('QuantumData Timing:',qd780_timing)
              print('QuantumData Pattern:',qd780_pattern)
    
              #use my_qd_generator class, need open/close serial everytime.
              #QD_Pattern_Gen=DEV_QD_GEN()
              #QD_Pattern_Gen.QD_Write(pattern)
              
          elif 'QD980' in self.case.loc[i]['Device_Control'].strip():
              QD980 = Telnet_QD980()
              qd980_timing = devCommand.split(',')[0]
              qd980_pattern = devCommand.split(',')[1]
                           
              QD980.do_telnet(qd980_timing.encode('utf-8'),qd980_pattern.encode('utf-8'))
              time.sleep(5)
              
              print("qd980 finished")
          
          
          elif 'EPCR3' in self.case.loc[i]['Device_Control'].strip():
              EPCR3 = PowerController()
              epcr3_port = devCommand.split(',')[0]
              epcr3_status = devCommand.split(',')[1]
              
              EPCR3.control_power(epcr3_port,epcr3_status)
              time.sleep(10)
              print("EPCR3 finished")
              
          elif 'ALISTREAMER' in self.case.loc[i]['Device_Control'].strip():
            aliStreamer = AliSteamerPlayer()
            streamName = devCommand.split(',')[0]
            freq = devCommand.split(',')[1]
            streamLoopTimes = devCommand.split(',')[2]
            print("Alitronika Streamer Settings: StreamName- %s Frequency-%s PlaybackLoopTimes-%s"%(streamName,freq,streamLoopTimes))
            aliStreamer.Ali_DTV_Player(streamName,freq,streamLoopTimes)
            print('The stream is playing...')          

     
      # Image Capture Start      
      
      if str(self.case.loc[i]['PIC_Capture'])!='nan':
         
          # select the capture device accoriding to the typical word in PIC_Capture column of test case
          # VX1-IMG with Unigraf UCD-2, CAM-IMG with camera for picture, CAM-VIDEO with camera for video
          if 'VX1-IMG' in self.case.loc[i]['PIC_Capture'].strip():
             
              
              #E01_SimpleCapture is UCD-2 simple capture program
              subprocess.call('E01_SimpleCapture.exe '+capFileName+' >>./Logs/UCD_log.txt',shell=True)
              
          elif 'CAM-IMG' in self.case.loc[i]['PIC_Capture'].strip():
              cap = CameraCapture()
              cap.open()
              cap.imageCapture(capDir+strIMStime,int(capTime))
              cap.close()
              
          elif 'CAM-VIDEO-END' in self.case.loc[i]['PIC_Capture'].strip():
              '''
              # Capture Video with OpenCV
              cap.open()
              # caputure video name and time(s) are divided with ","
              cap.videoCapture(capDir+strIMStime,capTime)
              cap.close()
              print 'The video record for the current case is finished!'
              '''
              # Capture AV with FFMPEG tool
              ffmpegCap.ffmpeg_video_record(CameraVDN,CameraADN,capDir+strIMStime+'.mkv',capTime,'"'+self.case.loc[i]['Test_Case_ID'].strip()+' '+self.case.loc[i]['Case_Description'].strip()+'"')
         
        #Test Result Ajudgement
        
        ### show Test Result in Table
        
      #Rest/UART Log Info comparision
      if str(self.case.loc[i]['Log_Ref'])!='nan':
          if str(self.case.loc[i]['Log_Capture'])!='nan':
              
              #Rest Info comparision
              if self.case.loc[i]['Log_Capture'].strip().split(']')[0].split('[')[1]=='REST':
                  restGet = restterminal()
                  restGetCommand=self.case.loc[i]['Log_Capture'].strip().split(']')[1]
                  print('REST Put Command Command:',restGetCommand)
          
                  fr=open(Auth_Token, "r")
                  self.read_auth_token=fr.readline().strip('\n')
                  fr.close()
               
                  restGet.read_dictionary()                             
                  #requests.packages.urllib3.disable_warnings()
                  restGetValue=restGet.parse_command(restGetCommand,self.read_auth_token)
                  print('Rest Get Value:%s'%restGetValue)
                  restGet.parse_command("restlog",self.read_auth_token)
                  
                  #print 'cherry test',self.case.iat[i,16] 
                  #print type(self.case.iat[i,16])
                  if self.case.loc[i]['Log_Ref'].strip()==restGetValue:
                      print("Compare the Rest Log") 
                      #Log_Result Column No.-16
                      self.case.iat[i,16]='Pass'
                  
                  else:
                      self.case.iat[i,16]='Fail'
              
              #UART Infor Comparision        
              elif self.case.loc[i]['Log_Capture'].strip().split(']')[0].split('[')[1]=='UART':
                  print("reserved for UART comparision")
                  keyWord = self.case.loc[i]['Log_Capture'].strip().split(']')[1]
                  keyWordFilter=ReFilter()
                  keyWordSearchResult=keyWordFilter.txtFilter(logFN,keyWord)   
                  
                  if keyWordSearchResult is not None: 
                    print("UART key word was found!")
                    self.case.iat[i,16]='Pass'
                  
                  else:
                    print('UART key word not found!')
                    self.case.iat[i,16]='Fail'
                     
      # Image comparision Start            
      if str(self.case.loc[i]['PIC_Ref'])!='nan':
          ref_image=self.case.loc[i]['PIC_Ref'].strip()+'.jpg'
          dst_image=capFileName+'.jpg'
          #dst_image='INPUT_002.jpg'
          print("The reference image name:",ref_image)
          print("The destination image name:",dst_image)
      
          myMatchImage=ImageMatch()
          self.PIC_result=myMatchImage.match(ref_image,dst_image,mode="ahash",win_size=32)
          print("Result: ham %d\t%s\t%s" % (self.PIC_result, ref_image, dst_image))     
     
          if self.PIC_result <=5:
              #PIC_Result Column No.-17
              self.case.iat[i,17]= str(self.PIC_result)+',Pass'
              print(self.case.iat[i,17])
          else:
              self.case.iat[i,17]= str(self.PIC_result)+',Fail'
              print(self.case.iat[i,17])   
      
      #Audio Comparision Start
      if str(self.case.loc[i]['Audio_Ref'])!='nan':
        print("reserved")
        
       
      # Show the execute result
      t = time.localtime(time.time())
      strIMSt = time.strftime("%I:%M:%S", t)
      #self.testcase.AppendText(strIMSt +' Result: ' + str(ret)+"\n\n")
      
      print("The test case waiting time:%s"%int(self.case.loc[i]['Time(s)']))
      time.sleep(int(self.case.loc[i]['Time(s)']))
     
      #close camera
      #cap.close()
      
      #Stop Dut's serial port
      self.serial_stop()
      print('DUT Serial Stop!')      
      
      #SW Upgrade check Start
       
      if self.case.loc[i]['Log_Ref']=='UART-SWUPGRADE': 
        
        print("SW upgrade information:")
        print(logFN)
        print('BuildNumber Val="'+gpus+'"')
        
        mytxtfilter=ReFilter()
        textSearchResult=mytxtfilter.txtFilter(logFN,'BuildNumber Val="'+gpus+'"')
        print("SW upgrade build number verification:%s"%textSearchResult)
        if textSearchResult is not None:
          #Upgrade sucessfully.
          print("Build %s was upgraded successfully!"%gpus)
          #Execute next test case
          i+=1
        else:
          
          retryTimes+=1
          if retryTimes>=2:
            print("SW Image Update failed after retrying %s times, test stopped!"%retryTimes)
            i=caseNum
          else:
            i=0
            print("Upgrade failed!Retry %s times!"%retryTimes)
      else:
        # Execute the next case
        i+=1
        
      if (i+1) <= caseNum:
        print("*****Case No.%s is starting*****"%(i+1))
        
      # One case is finished to run!
    
    #Save test result in excel table
    TestReportFileName='TestReport#'+gpus+'.xls'
    self.SaveResult('.\\TestReports\\'+TestReportFileName,self.case)  
    print("%s is generated!"%TestReportFileName)
    
    #Stop DUT and Device's UART
   
    #self.serial_stop()
    #print 'DUT Serial Stop!'
   
    
    self.qd_serial_stop()
    print('QD780 Serial Stop!')
    #cap.close()
    ret = 0 
    print('TEST FINISHED!')
    sys.exit()
    #os._exit()
    
if __name__ == '__main__':
    test = AutoDailyTest()
    #test.AutoLoadFile()
    
    #gpus="1279"
    gpus=sys.argv[1]
    print("Build No:",gpus)
    
    '''
    videoPath=".\\Video\\#"+gpus+"\\"
    print videoPath
    test.mkdir(videoPath)    
    '''
    
    #Load test case file
    
    #InitialTestFile='SW_upgrade.xlsx'
    InitialTestFile='Sanity_Test_SX7B_temp.xlsx'
    
    
    try:                       
      caseList = pd.read_excel(InitialTestFile, 'Test_Cases', index_col=None)
    except:
      print("ERROR: handle file %s"%InitialTestFile)
    
    #caseList.iat[0,7]='curl -o /cache/recovery/ota.zip http://10.86.9.134:8080/jenkins/view/SX8/job/P111_SX8B_sigma-full-ci_DailyBuild/'+gpus+'/artifact/rel_img/firefly-ota-F%23435.zip;10;uenv set bootmode forceupdate_cache;10;reboot;5'
    #caseList.iat[0,7]='curl -o /cache/recovery/ota.zip http://10.86.9.134:8080/jenkins/view/P111/job/P111_TV103_Sprint6_SX7B_BugfixBuild/'+gpus+'/artifact/rel_img/ota-GT%23'+gpus+'.zip;30;uenv set bootmode forceupdate_cache;10;reboot;180;cat /system/misc/atsc* |grep BuildNumber;10'
    #caseList.iat[0,7]='curl -o /cache/recovery/ota.zip http://10.86.9.134:8080/jenkins/view/P111/job/P111_TV103_Sprint6_SX7B_BugfixBuild/'+gpus+'/artifact/rel_img/ota-GT%23'+gpus+'.zip;30;uenv set bootmode forceupdate_cache;10;reboot;180;cat /system/misc/atsc* |grep BuildNumber;10'
    
    SanityTestFile=InitialTestFile.split('.')[0]+'_execution.xls'
   
    test.SaveResult(SanityTestFile,caseList)    
    
    test.RunCase(SanityTestFile)
    
   
    '''
    # If case needn't be updated, InitialTestFile can be read directly.
    test.RunCase(InitialTestFile)
    '''
   
    
    

# -*- coding: utf-8 -*-
import subprocess
import threading
from memory_profiler import profile
import wx
import sys
import os
import wx.html
import wx.grid
from wx import adv
#import struct
import time
import pandas as pd
import math
#import copy
from modules.log import logger
from modules.my_serial import SigmaSerial
from modules.MyGridTable import CustTableGrid
import wx.lib.buttons as buttons
from modules.my_imghash import ImageMatch
from modules.ReSTTerminal import restterminal
from modules.MyOTTCast import Tablet_Cast_Test
from modules.MyAirPlay import AIRPLAY
from modules.My_RestKey import Restkey_define
from modules.Tidevice import TideviceSetUp
from modules.MyRedRat import DEV_REDRAT
from modules.XML_Parsedata import XML_PARSE
from modules.my_net_controller import netIRControl
from modules.RedRatHubS import RedRatHubCmdSetUp
from modules.MyCamera import CameraCapture
from modules.my_qd980 import Telnet_QD980
from modules.TestCfgParse import TestCfgParse,CfgParse
from modules.my_epcr3 import PowerController
from modules.MyAliStreamer import AliSteamerPlayer
from modules.VsiliconAbout import VsiliconAbout
from modules.SetFileIni import SetFileIni

Auth_Token = "./Config/Auth_Token.txt"
AutoTestAppINI = './Config/AutoTestApp.INI'
File_Path = os.path.dirname(__file__)

class AutoTestAppPanel(wx.Panel):
    def __init__(self, parent, log):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.T = TideviceSetUp()
        self.RedRat = RedRatHubCmdSetUp()

        self.T.run()
        self.log = log
        self.cfg = CfgParse(AutoTestAppINI)
        # create timer for loop event
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
      
        """
        #############   Tree Layout
        """        
        self.tree = wx.TreeCtrl(self)
        #self.tree.AddRoot("root")
        
        # Bind some interesting events
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeActivated, self.tree)

        treeSizer = wx.BoxSizer(wx.VERTICAL)
        treeSizer.Add(self.tree, 1, wx.EXPAND|wx.ALL,5)
        
        """
        #############   Case Info Layout
        """

        box = wx.StaticBox(self, -1, '')        
        caseSizer=wx.StaticBoxSizer(box, wx.VERTICAL)
        #caseSizer=wx.BoxSizer(wx.VERTICAL)
        #wx.BoxSizer(wx.HORIZONTAL) #wx.FlexGridSizer(1, 5, hgap=5, vgap=5)        


        self.colIdx = {'Category':0, 'Case_ID':1, 'Case_Description':2,'Test_Seq':3,'Available':4, 'Rest_Control':5,
                          'IR_Seq':6, 'SerialCmd':7, 'Device_Control':8, 'Log_Capture':9, 'Log_Ref':10, 'PIC_Capture':11, 'PIC_Ref':12, 'Audio_Capture':13, 
                          'Audio_Ref':14,'Time(s)':15, 'Log_Result':16,'PIC_Result':17, 'Audio_Result':18, 'Test Result':19}        
        self.colLabels = ['Category', 'Case_ID', 'Case_Description','Test_Seq','Available', 'Rest_Control',
                          'IR_Seq', 'SerialCmd', 'Device_Control', 'Log_Capture', 'Log_Ref', 'PIC_Capture', 'PIC_Ref', 'Audio_Capture', 
                          'Audio_Ref','Time(s)', 'Log_Result','PIC_Result', 'Audio_Result', 'Test Result']        

        dataTypes = [wx.grid.GRID_VALUE_STRING, 
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_NUMBER,
                          wx.grid.GRID_VALUE_BOOL,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,                          
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING,
                          wx.grid.GRID_VALUE_STRING
                          ]        
       
       
        self.table = CustTableGrid(self, log, self.colLabels, dataTypes)
           
          
        self.auth_token=""
        self.read_auth_token=""
        
        boxExecute = wx.StaticBox(self, -1, 'ExcuteResult')
        boxExecute.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
        sizerExecute = wx.StaticBoxSizer(boxExecute, wx.HORIZONTAL)
        self.testcase = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        self.testcase.SetFont(wx.Font(10,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
        #change 44th to 52th charactors style
        #self.testcase.SetStyle(44,52,wx.TextAttr("white","black"))
        self.testcase.SetDefaultStyle(wx.TextAttr("white","forest green"))
    
        sizerExecute.Add(self.testcase, 1, wx.EXPAND|wx.ALL,5)
        
        boxSerialMsg = wx.StaticBox(self, -1, 'Serial Output')
        boxSerialMsg.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
        sizerSerialMsg=wx.StaticBoxSizer(boxSerialMsg, wx.HORIZONTAL)
        self.serialmsg = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        sizerSerialMsg.Add(self.serialmsg, 1, wx.EXPAND|wx.ALL,5)
        
        boxSerialCmd = wx.StaticBox(self, -1, 'Command2Serial')
        boxSerialCmd.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
        sizerSerialCmd=wx.StaticBoxSizer(boxSerialCmd, wx.HORIZONTAL)
        self.tcSerialCmd = wx.TextCtrl(self, -1, '')
        self.btWrite2Serial = wx.Button(self, -1, "WriteToSerial")
        self.btWrite2Serial.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnSendCommandViaSerial, self.btWrite2Serial)
        sizerSerialCmd.Add(self.tcSerialCmd, 5, wx.EXPAND|wx.ALL,5)
        sizerSerialCmd.Add(self.btWrite2Serial, 1, wx.EXPAND|wx.ALL,5)
        
        caseSizer.Add(self.table, 4, wx.EXPAND|wx.ALL|wx.FIXED_MINSIZE,1)
        caseSizer.Add(sizerSerialMsg, 3, wx.EXPAND|wx.ALL, 1)
        caseSizer.Add(sizerExecute, 2, wx.EXPAND|wx.ALL, 1)
        caseSizer.Add(sizerSerialCmd, 1, wx.EXPAND|wx.ALL, 1)
                
        """
        #############   Command Layout
        """
        #box1 = wx.StaticBox(self, -1, "Command")
        #cmdSizer=wx.StaticBoxSizer(box1, wx.VERTICAL)
        cmdSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.btConnectSerial = buttons.GenToggleButton(self, -1, "DUTSerialON")
        self.btConnectSerial.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnConnectSerial, self.btConnectSerial)
        #self.btConnectSerial.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,False))
        self.btConnectSerial.SetBezelWidth(2)
        
        self.btConnectDevice = buttons.GenToggleButton(self, -1, "DEVSerialON")
        self.btConnectDevice.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnConnectDevice, self.btConnectDevice)
        #self.btConnectDevice.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.btConnectDevice.SetBezelWidth(2)

        self.btConnectUCD = buttons.GenToggleButton(self, -1, "ConnectUCD")
        self.btConnectUCD.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnConnectUCD, self.btConnectUCD)
        #self.btConnectUCD.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.btConnectUCD.SetBezelWidth(2)
        
        self.deleteCase = wx.Button(self, -1, "Delete")
        self.deleteCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnDeleteRows, self.deleteCase)

        self.ConfigCase = wx.Button(self, -1, "Setting")
        self.ConfigCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.SettingRunRows, self.ConfigCase)

        self.RedRatRunCase = wx.Button(self, -1, "RedRatRun")
        self.RedRatRunCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.RedRatRunRows, self.RedRatRunCase)

        self.RedRatKillCase = wx.Button(self, -1, "RedRatKill")
        self.RedRatKillCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.RedRatKillRows, self.RedRatKillCase)

        self.selectAll = buttons.GenToggleButton(self, -1, "SelectAll")
        self.selectAll.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, self.selectAll)
        #self.selectAll.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.selectAll.SetBezelWidth(2)
        #self.connect.SetBackgroundColour("Red")
        
        self.runCase = wx.Button(self, -1, "Run")
        self.runCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnRunCase, self.runCase)
        
        self.stopCurrCase = wx.Button(self, -1, "Stop")
        self.stopCurrCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnStopCurrCase, self.stopCurrCase)
        
        self.nextCase = wx.Button(self, -1, "Next")
        self.nextCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnNextCase, self.nextCase)
        
        self.PauseCase = buttons.GenToggleButton(self, -1, "Pause")
        self.PauseCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.PauseCase.SetBezelWidth(2)
        self.Bind(wx.EVT_BUTTON, self.OnPause, self.PauseCase)
        
        self.stopCase = wx.Button(self, -1, "Stop")
        self.stopCase.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.stopCase)
        self.PauseCase.Enable(False)
        self.stopCase.Enable(False)

        self.loop = wx.Button(self, -1, "Loop")
        self.loop.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnLoop, self.loop)


        self.load = wx.Button(self, -1, "Open Excel...")
        self.load.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        # self.load.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, self.load)

        self.Save = wx.Button(self, -1, "Save Excel")
        self.Save.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.OnSave,self.Save)

        self.openvideo = wx.Button(self, -1, "Open Video... ")
        self.openvideo.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        # self.load.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.Onpenvideo, self.openvideo)

        self.clearvideo = wx.Button(self, -1, "Clear Video")
        self.clearvideo.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.Bind(wx.EVT_BUTTON, self.Onclearvideo, self.clearvideo)
        
        
        #self.PauseCase.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        #self.PauseCase.SetBezelWidth(2)
        #self.PauseCase.SetBackgroundColour("Red")
        
        #connect
        boxConnect = wx.StaticBox(self, -1, 'Connect ON/OFF')
        boxConnect.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False))
        sizerConnect=wx.StaticBoxSizer(boxConnect, wx.VERTICAL)
        sizerConnect.Add(self.btConnectSerial, 1, wx.EXPAND|wx.ALL,5)
        sizerConnect.Add(self.btConnectDevice, 1, wx.EXPAND|wx.ALL,5)
        sizerConnect.Add(self.btConnectUCD, 1, wx.EXPAND|wx.ALL,5)
        
        # edit
        boxEdit = wx.StaticBox(self, -1, 'Edit')
        boxEdit.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False))
        sizerEdit=wx.StaticBoxSizer(boxEdit, wx.VERTICAL)
        
        sizerEdit.Add(self.deleteCase, 1, wx.EXPAND|wx.ALL,5)
        sizerEdit.Add(self.selectAll, 1, wx.EXPAND|wx.ALL,5)

        # Setting
        seTTing = wx.StaticBox(self, -1, 'Setting')
        seTTing.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        sizerSetting = wx.StaticBoxSizer(seTTing, wx.VERTICAL)
        sizerSetting.Add(self.ConfigCase, 1, wx.EXPAND | wx.ALL, 5)

        # RedRatHub
        boxRedRat = wx.StaticBox(self, -1, 'RedRatHub')
        boxRedRat.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        sizerRedRat = wx.StaticBoxSizer(boxRedRat, wx.VERTICAL)

        sizerRedRat.Add(self.RedRatRunCase, 1, wx.EXPAND | wx.ALL, 5)
        sizerRedRat.Add(self.RedRatKillCase, 1, wx.EXPAND | wx.ALL, 5)
        
        # run
        boxRun = wx.StaticBox(self, -1, 'RunCase')
        boxRun.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False))
        sizerRun=wx.StaticBoxSizer(boxRun, wx.VERTICAL)
        
        sizerRun.Add(self.runCase, 1, wx.EXPAND|wx.ALL,5)
        sizerRun.Add(self.stopCurrCase, 1, wx.EXPAND|wx.ALL,5)
        sizerRun.Add(self.nextCase, 1, wx.EXPAND|wx.ALL,5)
        
        boxLoop = wx.StaticBox(self, -1, 'LoopTest')
        boxLoop.SetFont(wx.Font(8,wx.FONTFAMILY_SWISS,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False))
        sizerLoop=wx.StaticBoxSizer(boxLoop, wx.VERTICAL)
        
        sizerLoop.Add(self.loop, 1, wx.EXPAND|wx.ALL,5)
        sizerLoop.Add(self.PauseCase, 1, wx.EXPAND|wx.ALL,5)
        sizerLoop.Add(self.stopCase, 1, wx.EXPAND|wx.ALL,5)

        # Excel File
        fileOp = wx.StaticBox(self, -1, 'Excel File')
        fileOp.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        sizerFileOp = wx.StaticBoxSizer(fileOp, wx.VERTICAL)

        sizerFileOp.Add(self.load, 1, wx.EXPAND|wx.ALL,5)
        sizerFileOp.Add(self.Save, 1, wx.EXPAND|wx.ALL,5)

        # LOG File
        logfileOp = wx.StaticBox(self, -1, 'Log File')
        logfileOp.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        sizerlogfileOp = wx.StaticBoxSizer(logfileOp, wx.VERTICAL)

        sizerlogfileOp.Add(self.openvideo, 1, wx.EXPAND | wx.ALL, 5)
        sizerlogfileOp.Add(self.clearvideo, 1, wx.EXPAND | wx.ALL, 5)


        cmdSizer.Add(sizerConnect, 0, wx.EXPAND|wx.ALL, 5)
        cmdSizer.Add(sizerSetting, 0, wx.EXPAND|wx.ALL, 5)
        cmdSizer.Add(sizerRedRat, 0, wx.EXPAND | wx.ALL, 5)
        cmdSizer.Add(sizerEdit, 0, wx.EXPAND|wx.ALL, 5)        
        cmdSizer.Add(sizerRun, 0, wx.EXPAND|wx.ALL, 5)        
        cmdSizer.Add(sizerLoop, 0, wx.EXPAND|wx.ALL, 5)
        cmdSizer.Add(sizerFileOp, 0, wx.EXPAND | wx.ALL, 5)
        cmdSizer.Add(sizerlogfileOp, 0, wx.EXPAND | wx.ALL, 5)


        # programme layout        
        
        dtvSizer = wx.BoxSizer(wx.HORIZONTAL)
        dtvSizer.Add(treeSizer, 2, wx.EXPAND|wx.ALL, 5)
        dtvSizer.Add(caseSizer, 10, wx.EXPAND|wx.ALL, 5)
        dtvSizer.Add(cmdSizer, 1, wx.EXPAND|wx.ALL, 5) 
        
        # read progreaminfo file name from the configuration file
        self.AutoTestCfgInfo()
        
        # auto-load and parse the stream program information
        self.AutoLoadFile()
                
        """
        #############  Whole Layout
        """
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)                
        mainSizer.Add(dtvSizer, 3, wx.EXPAND|wx.ALL, 5)
                
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        #mainSizer.SetSizeHints(self) 
        
        # EVT_CLOSE is not triggerred, which only is triggered in the top window
        #self.Bind(wx.EVT_CLOSE,  self.OnExit)
        
        self.my_serial = None
        self.qd_serial = None
        
    def Log(self, msg):
        #self.log.Log(msg)
        self.testcase.AppendText(msg+"\n")
    
    def AutoTestCfgInfo(self):
        '''
        parse the target board socket server address and its port
        '''

        self.AutoTestInfoFile = self.cfg.GetCfgInfo("AUTOTEST","AutoTestCfg")
        # cfgList = ''
        # try:
        #     with open(AutoTestAppINI, 'r') as f:
        #         cfgList = [line.strip() for line in f.readlines()]
        #         #self.fileList
        #         f.close()
        # except Exception as e:
        #     self.Log(str(e.args))
        #
        # self.AutoTestInfoFile = 'Sanity_Test.xlsx'
        # for item in cfgList:
        #     if item.startswith('AutoTestCfg'):
        #         self.AutoTestInfoFile = item.split("=")[1]
        print('test case file is:',self.AutoTestInfoFile)
            
    def AutoLoadFile(self):
        try:
            self.ReadAutoTestInfo(self.AutoTestInfoFile)
        except Exception as e:
            self.Log("ERROR: handle file %s" % self.AutoTestInfoFile)
            self.Log("ERROR: handle file %s" % str(e.args))
            return

        # remove the previous notes on root 
        self.tree.DeleteAllItems()
        
        root = self.tree.AddRoot("AutoTestCases") 
        self.AddAutoTestInfoToTree(root, self.sources)
        self.tree.ExpandAll()
        
        self.tree.SetItemBold(root,bold=True)
       
        
    def OnAutoLoadFile(self, event):
        self.AutoLoadFile()
        
    wildcard = "TestCases files (*.xlsx;*.xls)|*.xlsx;*.xls|All files (*.*)|*.*"

    def OnLoadFile(self, event):
        dlg = wx.FileDialog(self, "Open file...", os.getcwd(),
                           style=wx.FD_OPEN, wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.AutoTestInfoFile = dlg.GetPath()
            #self.log.write("Load file: ", self.filename)
            self.Log( "Load file: %s" % self.AutoTestInfoFile )
            
            self.AutoLoadFile()
            
        dlg.Destroy()
        event.Skip()

    def OnSave(self,event):
        file_wildcard="Test_Cases files(*.xlsx)|*.xlsx|files(*.xls)|*.xls|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            "Save file as ...",
                            os.getcwd(),
                            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                            wildcard = file_wildcard)

        if dlg.ShowModal()== wx.ID_OK:
            filename = dlg.GetPath()

            if not os.path.splitext(filename)[1]:#if no suffix
                filename = filename+'.xlsx'
            self.SaveResult(filename)

        dlg.Destroy()
        event.Skip()

    def SaveResult(self,filename):

        table = []
        rows = self.table.GetTableRows()
        for i in range (rows):
            table.append(self.table.GetRowValueFromTable(i))

        df=pd.DataFrame(table,columns = self.colLabels)

        writer=pd.ExcelWriter(filename)
        df.to_excel(writer,'Test_Cases',index = False)
        writer.save()
        writer.close()
        
    def OnConnectSerial(self, event):   
        global board_port
        cfgList = ''
        try:            
            with open(AutoTestAppINI, 'r') as f:
                cfgList = [line.strip() for line in f.readlines()]
                ###print(cfgList)
                logger.info(cfgList)
                f.close()
        except Exception as e:
            self.Log(str(e.args))

        for item in cfgList:
            if item.startswith('Board_PORT'):
                board_port=item.split("=")[1]
                ##print(board_port)
                logger.info(board_port)

        if self.my_serial is None:
            self.my_serial = SigmaSerial()
                  
        button = event.GetEventObject()
        if button.GetValue():
            self.serial_start(board_port)
            if not self.my_serial.isOpen():
                button.SetLabel("Fail,TryAgain")                    
            else:             
                button.SetLabel("DUTSerialOFF")  
            
            #button.SetFocus()
            button.Refresh()
        else:
            self.serial_stop()
            button.SetLabel("DUTSerialON")            
            #button.SetBackgroundColour("Red")
            
        event.Skip()
        
    def OnSendCommandViaSerial(self, event):
        if self.alive:
            try:
                snddata=self.tcSerialCmd.GetValue()
                self.my_serial.writes(snddata)
                # self.my_serial.writes(snddata.encode('utf-8'))
                self.serialmsg.AppendText('#' + snddata+'\n')
                ##print('SEND CMD: '+' '+ time.strftime("%Y-%m-%d %X") + ' ' + snddata)
                logger.info('SEND CMD: '+' '+ time.strftime("%Y-%m-%d %X") + ' ' + snddata)

            except Exception as e:
                ##print("error")
                logger.info("error")
                logger.info(str(e.args))

        event.Skip()
        
    def serial_start(self,portname): 
        
        if self.my_serial is None:
            self.my_serial = SigmaSerial()
                
        try:            
            self.my_serial.open(portname)
                 
            if self.my_serial.isOpen():
                #self.waitEnd = threading.Event()
                self.alive = True
                
                self.thread_read = threading.Thread(target=self.serial_reader)
                self.thread_read.setDaemon(True)
                
                self.thread_read.start()
                return True
            else:
                ##print('Serial has not been started\n')
                logger.info('Serial has not been started\n')
                return False
        except Exception as e:
            self.Log(str(e.args))
            return False
        
    def serial_reader(self):
        while self.alive:
            try:
                '''
                n=self.my_serial.inWaiting()
                data=''
                if n:
                    data= self.my_serial.read(n).decode('utf-8')             
                    ##print ('recv'+' '+time.strftime("%Y-%m-%d %X")+' '+data.strip())
                    ##print (time.strftime("%Y-%m-%d %X:")+data.strip(),file=self.rfile)
                    self.show.AppendText(data.strip()+'\n')
                    if len(data)==1 and ord(data[len(data)-1])==113: #收到字母q，程序退出
                        break
                '''
                data = self.my_serial.readlines().encode('utf-8')
                if len(data) > 1:
                    self.serialmsg.AppendText(data.strip()+b'\n')
                    logfile=open('.\\Logs\\DUT_log.txt','a+')
                    logfile.write(data.decode('utf-8'))
                    logfile.flush()
                    logfile.close()
            except Exception as e:
                self.Log(str(e.args))
 
        #self.waitEnd.set()
        self.alive = False

    def serial_stop(self):
        #self.thread_read.join()
        if not self.my_serial is None:
            self.alive = False
            if self.my_serial.isOpen():
                self.my_serial.close()
           
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
                #print("QD Serial has not been started\n")
                logger.info("QD Serial has not been started\n")
                return False
        except Exception as e:
            self.Log(str(e.args))
            return False

    def qd_serial_reader(self):
        while self.alive:
            try:
                '''
                n=self.my_serial.inWaiting()
                data=''
                if n:
                    data= self.my_serial.read(n).decode('utf-8')             
                    ##print ('recv'+' '+time.strftime("%Y-%m-%d %X")+' '+data.strip())
                    ##print (time.strftime("%Y-%m-%d %X:")+data.strip(),file=self.rfile)
                    self.show.AppendText(data.strip()+'\n')
                    if len(data)==1 and ord(data[len(data)-1])==113: #收到字母q，程序退出
                        break
                '''
                data = self.qd_serial.readlines().decode('utf-8')
                if len(data) > 1:
                    self.serialmsg.AppendText(data.strip()+'\n')
            except Exception as e:
                self.Log(str(e.args))
 
        #self.waitEnd.set()
        self.alive = False



    def qd_serial_stop(self):
        #self.thread_read.join()
        if not self.qd_serial is None:
            self.alive = False
            if self.qd_serial.isOpen():
                self.qd_serial.close()
           
      
    def OnConnectDevice(self, event):

        global dev_qd_port
        cfgList = ''
        try:            
            with open(AutoTestAppINI, 'r') as f:
                cfgList = [line.strip() for line in f.readlines()]
                #print(cfgList)
                logger.info(cfgList)
                f.close()
        except Exception as e:
            self.Log(str(e.args))

        for item in cfgList:
            if item.startswith('DEV_QD_PORT'):
                dev_qd_port=item.split("=")[1]
                #print(dev_qd_port)
                logger.info(dev_qd_port)

        if self.qd_serial is None:
            self.qd_serial = SigmaSerial()
                  
        button = event.GetEventObject()
        if button.GetValue():
            self.qd_serial_start(dev_qd_port)
            if not self.qd_serial.isOpen():
                button.SetLabel("Fail,TryAgain")                    
            else:             
                button.SetLabel("DEVSerialOFF")
                #pattern = 'IMGL ColorBar'
                #self.my_serial.write(pattern)
                #self.my_serial.write('IMGU')
            #button.SetFocus()
            button.Refresh()
        else:
            self.qd_serial_stop()
            button.SetLabel("DEVSerialON")            
            #button.SetBackgroundColour("Red")
            
        event.Skip()

    def OnConnectUCD(self, event):
       
        event.Skip()

    def ReadAutoTestInfo(self, filename):
        '''
        Return:
        {self.Source:{souce_name:pd<source cases,...>}
        '''
        # read Source Sheet to get the source list firstly
        self.df = pd.read_excel(filename,sheet_name='Test_Cases', index_col=None)
                
        ##print self.df.loc[0]['Rest_Control']
        ##print ('Parse excel data:\n',self.df)
        #delete the repeat element
        source_list = list(set(list(self.df.loc[:,'Category'])))
                
        self.sources = {}
        for source in source_list:
            if source not in self.sources:
                self.sources[source] = []
            for idx in self.df.index:
                if source in self.df.loc[idx,'Category']:
                    self.sources[source].append(self.df.loc[idx,'Case_ID'])
                  
    def AddAutoTestInfoToTree(self, root, sourceInfo):
        #print(sourceInfo)
        logger.info(sourceInfo)
        #print(list(sourceInfo.keys()))
        logger.info(list(sourceInfo.keys()))
        for key in list(sourceInfo.keys()):  # key is source name
            sourceItem = self.tree.AppendItem(root, key)
            for case in sourceInfo[key]:
                self.tree.AppendItem(sourceItem, case)                
                
    def OnTimer(self, event):
        
        if self.TotalLoopTime > 0:
            if self.loopTime == 0:
                t = time.localtime(time.time())
                strIMSt = time.strftime("%I:%M:%S", t) 
                #print("test start:",strIMSt)
                logger.info("test start:",strIMSt)

                if self.loopCurr is not None:
                    self.loopTable.append(self.loopCurr)
                    
                self.loopCurr = self.loopTable.pop(0)
                
                #self.Log("Time:" + strIMSt +  str(self.loopCurr))
                self.Log("Next Case:" + str(self.loopCurr[1]) +' '+str(self.loopCurr[2]))               
            
                try:
                    
                    self.RunCase(self.loopCurr)
                except Exception as e:
                    #print(e)
                    logger.info(e)
                    self.Log( "Error: %s" %str(e.args) )
                    self.OnStop()
                     
                self.loopTime = int(self.loopCurr[self.colIdx['Time(s)']])
                self.TotalLoopTime=self.TotalLoopTime-self.loopTime
                self.Log("The remained test time for test cycle(s):"+str(self.TotalLoopTime))
                self.rowNumber +=1
                
            else:
                self.loopTime -= 1
                #print("The remained test time for the current test case:",self.loopTime)
                logger.info("The remained test time for the current test case:",self.loopTime)
                #print("The cycle toltal test time:",self.TotalLoopTime)
                logger.info("The cycle toltal test time:",self.TotalLoopTime)

        else:
            self.OnStop()
            self.table.ClearSelection()


        '''
        attr1=wx.grid.GridCellAttr()
        attr1.SetBackgroundColour("light blue")
        attr2=wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("pink")        
        #self.table.SetRowAttr(1,attr)  
        Rows = self.table.GetSelectedRowsFromTable()
        
        if self.TotalLoopTime >0:
            if ( self.loopTime == 0 ):
                t = time.localtime(time.time())
                strIMSt = time.strftime("%I:%M:%S", t) 
                #print "test start:",strIMSt
                
                if self.loopCurr is not None:
                    self.loopTable.append(self.loopCurr)
                    
                self.loopCurr = self.loopTable.pop(0)
                #self.Log("Time:" + strIMSt +  str(self.loopCurr))
                
                for row in Rows:
                    table = self.table.GetRowValueFromTable(row)
                    if self.loopCurr == table:
                        self.table.SetRowAttr(row,attr1)
                    
            
                try:
                    self.RunCase(self.loopCurr)
                except Exception:
                    self.OnStop(event)    
                     
                self.loopTime = int(self.loopCurr[self.colIdx['Time(s)']])
                self.TotalLoopTime=self.TotalLoopTime-self.loopTime
                self.Log("The remained test time for test cycle:"+str(self.TotalLoopTime))
                
            else:
                self.loopTime -= 1
                
                #print "The remained test time(m) for the current test case:",self.loopTime
                #if self.loopTime== 1:
                    #self.table.SetRowAttr(self.row,attr2)
        '''                           
                  
    def OnPause(self, event):
        button = event.GetEventObject()
        if button.GetValue():  
            self.timer.Stop()
            button.SetLabel("Resume")
            #button.SetBackgroundColour("Yellow")            
        else:
            self.timer.Start(1000)              
            button.SetLabel("Pause")
            #button.SetBackgroundColour("Red")
    
    def OnLoop(self, event):
        '''
        Load Loop Table, and Add the test time if no
        start the timer to trigger the test
        '''
        self.loop.Enable(False)
        self.loop.SetLabel("Looping")
        self.loopTable = []
        self.TotalLoopTime=0
        self.OneCycleLoopTime=0
                
        Rows = self.table.GetSelectedRowsFromTable()
        if not Rows:
            self.ShowMessage1()
        for row in Rows:
            table = self.table.GetRowValueFromTable(row)

            '''
            attr=wx.grid.GridCellAttr()
            attr.SetBackgroundColour("light blue")
            self.table.SetRowAttr(row,attr)            
            '''
            ##print type(table[self.colIdx['Avail']]), table[self.colIdx['Avail']]
            # only add the avail case to the loop
            if table[self.colIdx['Available']] != '' and table[self.colIdx['Available']] != 0 and table[self.colIdx['Available']] != '0':
                self.loopTable.append(table)
                if table[self.colIdx['Time(s)']] == '':
                    #print('The test case runtime is null, set the default time to 3 seconds')
                    logger.info('The test case runtime is null, set the default time to 3 seconds')
                    table[self.colIdx['Time(s)']] = 3
                self.OneCycleLoopTime=self.OneCycleLoopTime+int(table[self.colIdx['Time(s)']])
        #print("The loop time for one cycle test is (s):",self.OneCycleLoopTime)
        logger.info("The loop time for one cycle test is (s):{}".format(self.OneCycleLoopTime))
        #print("Loop Test case table:",self.loopTable)
        logger.info("Loop Test case table:{}".format(self.loopTable))


        # set loop time for each selected case
        defaultLoopTime = 0
        defaultLoopCycles = 0

        for table in self.loopTable:
            if table[self.colIdx['Time(s)']] == '':
                if defaultLoopTime == 0:
                    dlg = wx.TextEntryDialog(None, "Set Default Loop Time",
                                      'Config',
                                      "3", style=wx.OK|wx.CANCEL)
                    if dlg.ShowModal() == wx.ID_OK:
                        defaultLoopTime = int(dlg.GetValue())
                    else:
                        defaultLoopTime = 3
                    dlg.Destroy()

                table[self.colIdx['Time(s)']] = defaultLoopTime

        dlg_loopcycles = wx.TextEntryDialog(None,"Set Loop Times",
                                           'Config',
                                           "1",style=wx.OK|wx.CANCEL)
        if dlg_loopcycles.ShowModal()==wx.ID_OK:
            defaultLoopCycles = int(dlg_loopcycles.GetValue())
        else:
            defaultLoopCycles = 1
        dlg_loopcycles.Destroy()
        self.TotalLoopTime=self.OneCycleLoopTime*defaultLoopCycles
        #print("Total %d test cycle(s) need be executed and need test time:%ds" % (defaultLoopCycles,self.TotalLoopTime))
        logger.info("Total %d test cycle(s) need be executed and need test time:%ds" % (defaultLoopCycles,self.TotalLoopTime))

        self.table.AutoSizeColumns(True)

        self.Log('-' * 60)
        self.Log("Loop Test Case:")
        self.Log("Selected Rows: " + str(Rows))
        for case in self.loopTable:
            self.Log(str(case))
        self.Log('-' * 60)

        self.runCase.Enable(False)
        self.stopCurrCase.Enable(False)
        self.nextCase.Enable(False)

        self.PauseCase.Enable(True)
        self.stopCase.Enable(True)
        self.loopTime = 0
        self.loopCurr = None
        self.rowNumber = 0
        self.timer.Start(1000)

    def OnStop(self):
        # stop the timer and clear the loop table
        self.timer.Stop()  
        del self.loopTable
        self.PauseCase.SetValue(0)
        self.PauseCase.SetLabel("Pause")
        self.PauseCase.Enable(False)
        self.stopCase.Enable(False)
        self.runCase.Enable(True) 
        self.stopCurrCase.Enable(True) 
        self.nextCase.Enable(True) 
        self.loop.Enable(True)
        self.loop.SetLabel("Loop")   
        
    def StopPrevCase(self):
        pass
            
    def OnSelectAll(self, event):
        button = event.GetEventObject()
        if button.GetValue():
            self.Log( 'select all' )
            self.table.SelectAll()              
            button.SetLabel("UnSelectAll")  
            #button.SetBackgroundColour("Yellow")              
            #button.SetFocus()
            
        else:  
            self.Log( 'un-select all' )
            self.table.ClearSelection()
            button.SetLabel("SelectAll")
            #button.SetBackgroundColour("Red")

        button.Refresh()
        
        event.Skip()    
       
    def RunCase(self, case):        
        # self.StopPrevCase()
        
        # Run test Case
        t = time.localtime(time.time())
        strIMSt = time.strftime("%I:%M:%S", t)
        strIMStime=time.strftime("-%Y-%m-%d-%H-%M-%S", t)
        
        #self.testcase.AppendText('\n'+ strIMSt +' Execute Case: ' + str(case)+"\n")
        self.testcase.AppendText('\n'+ strIMSt +' Execute Case: ' + str(case[self.colIdx['Case_ID']])+'  '+str(case[self.colIdx['Case_Description']])+"\n")
        
                
        # Camera Thread Creation
               
        if case[self.colIdx['PIC_Capture']].strip()!='':
            capFileName =''
            capTime=0  
            # the location to save picture and video
            videoPath='.\\Video\\' 
            
            # CameraCfg=TestCfgParse()
            # CameraVDN=CameraCfg.GetTestCfgInfo("Camera_Video_Device_Name")
            # CameraADN=CameraCfg.GetTestCfgInfo("Camera_Audio_Device_Name")
            
            '''
            # enable if using ffmpeg for video record
            ffmpegCap=FFMpegCapture()
            ffmpegCap.cameraInit(CameraVDN)
            '''       
            
            #MyCamera class instance with opencv
            cap = CameraCapture()  
            
            # get the capture file name
            capFileName = case[self.colIdx['PIC_Capture']].strip().split(']')[1].split(',')[0]
            capTime = case[self.colIdx['PIC_Capture']].strip().split(']')[1].split(',')[1] 
            capDir=videoPath+capFileName 
            
            #ffmpeg video record command
            #self.thread_camera=threading.Thread(target=ffmpegCap.ffmpeg_video_record,args=(CameraVDN,CameraADN,capDir+strIMStime+'.mkv',capTime,'"'+case[self.colIdx['Case_ID']].strip()+' '+case[self.colIdx['Case_Description']].strip()+'"'))
            self.thread_camera=threading.Thread(target=cap.videoCapture,args=(capDir+strIMStime,capTime))
            # print(self.thread_camera)
            #print("Camera thread status before next case:")
            logger.info("Camera thread status before next case: {}".format(self.thread_camera.is_alive()))
            #print(self.thread_camera.is_alive())
            # logger.info(self.thread_camera.is_alive())

            if 'CAM-VIDEO-START' in case[self.colIdx['PIC_Capture']].strip():
                #print('***********************Start Video Capture****************************************')
                logger.info('***********************Start Video Capture****************************************')
                # open the camera
                cap.open()     
                #print("camera is opened")
                logger.info("camera is opened")
                #self.thread_camera=threading.Thread(target=cap.videoCapture,args=(capDir+strIMStime,capTime))
                self.thread_camera.start() 
                #print("Camera thread status:")
                logger.info("Camera thread status:")
                #print(self.thread_camera.isAlive())
                logger.info(self.thread_camera.isAlive())

        else:
            #print('***********************No Video Capture At this time*******************************')
            logger.info('***********************No Video Capture At this time*******************************')

        
        # Rest/Cast Control Start
        if case[self.colIdx['Rest_Control']].strip()!='':
            
            #print("Current Function:",case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1])
            logger.info("Current Function:{}".format(case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]))

            if case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]=='REST':
                rest = restterminal()
                restCommand=case[self.colIdx['Rest_Control']].strip().split(']')[1]
                #print('RESTCommand:',restCommand)
                logger.info('RESTCommand:{}'.format(restCommand))

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
                    #print('restValue:',restValue)
                    logger.info('restValue:{}'.format(restValue))
                    time.sleep(3)
                    rest.parse_command("restlog",self.read_auth_token)

            elif case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]=='CAST':
                                
                OTTCast = Tablet_Cast_Test()
               
                #Parse OTT name, movie name and playback time.
                castCommand=case[self.colIdx['Rest_Control']].strip().split(']')[1]
                OTTName=castCommand.strip().split(',')[0]
                MovieName=castCommand.strip().split(',')[1]
                PlayBackTime=castCommand.strip().split(',')[2]
                
                #print('CAST',OTTName)
                logger.info('CAST',OTTName)
                #print('MovieName',MovieName)
                logger.info('MovieName',MovieName)
                #print('PlayBackTime',PlayBackTime)
                logger.info('PlayBackTime',PlayBackTime)

                if OTTName=='Netflix':
                    OTTCast.Cast_Netflix(OTTName,MovieName,PlayBackTime)
                elif OTTName=='YouTube':
                    OTTCast.Cast_Youtube(OTTName,MovieName,PlayBackTime)
                    #print('Youtube movie:',MovieName)
                    logger.info('Youtube movie:',MovieName)
                elif OTTName=='Disney+':
                    OTTCast.Cast_DisneyPlus(OTTName,MovieName,PlayBackTime)
                    #print('DisneyPlus movie:',MovieName)
                    logger.info('DisneyPlus movie:',MovieName)
                elif OTTName=='PlayMusic':
                    OTTCast.Cast_PlayMusic(OTTName,MovieName,PlayBackTime)
                    #print('PlayMusic movie:',MovieName)
                    logger.info('PlayMusic movie:',MovieName)
                elif OTTName=='Hulu':
                    OTTCast.Cast_Hulu(OTTName,MovieName,PlayBackTime)
                    #print('Hulu movie:',MovieName)
                    logger.info('Hulu movie:',MovieName)

            elif case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1] == 'AIRPLAY':

                # APPboot = APP()


                APP = AIRPLAY()

                # Parse OTT name, movie name and playback time.
                castCommand = case[self.colIdx['Rest_Control']].strip().split(']')[1]
                OTTName = castCommand.strip().split(',')[0]
                MovieName = castCommand.strip().split(',')[1]
                PlayBackTime = castCommand.strip().split(',')[2]

                #print('AIRPLAY', OTTName)
                logger.info('AIRPLAY', OTTName)
                #print('MovieName', MovieName)
                logger.info('MovieName', MovieName)
                #print('PlayBackTime', PlayBackTime)
                logger.info('PlayBackTime', PlayBackTime)


                if OTTName == 'Netflix':
                    APP.APPlaunch("start","Netflix")
                    # APPstart = AIRPLAY()
                    APP.netflixuser()
                    APP.netflixcast(MovieName, PlayBackTime)
                    APP.APPlaunch("stop", "Netflix")
                    #print('Netflix movie:', MovieName)
                    logger.info('Netflix movie:', MovieName)

                elif OTTName == 'YouTube':
                    APP.APPlaunch("start", "YouTube")
                    # APPstart = AIRPLAY()
                    APP.youtubecast(MovieName, PlayBackTime)
                    APP.APPlaunch("stop", "YouTube")
                    #print('YouTube movie:', MovieName)
                    logger.info('YouTube movie:', MovieName)

                elif OTTName == 'YouTubeairplay':
                    APP.APPlaunch("start", "YouTube")
                    # APPstart = AIRPLAY()
                    APP.youtubeairplay(MovieName, PlayBackTime)
                    APP.APPlaunch("stop", "YouTube")
                    #print('YouTube movie:', MovieName)
                    logger.info('YouTube movie:', MovieName)

                elif OTTName == 'AppleTV':
                    APP.APPlaunch("start", "AppleTV")
                    # APPstart = AIRPLAY()
                    APP.appletvairplay(MovieName, PlayBackTime)
                    APP.APPlaunch("stop", "AppleTV")
                    #print('AppleTV movie:', MovieName)
                    logger.info('AppleTV movie:', MovieName)

            elif case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]=='REMOTEKEY':
                restKey=Restkey_define()
                restKeyCommand=case[self.colIdx['Rest_Control']].strip().split(']')[1]
                #print('Rest Key Commands:%s'%restKeyCommand)
                logger.info('Rest Key Commands:%s'%restKeyCommand)

                if ":" in restKeyCommand:
                    #print('Execute Remote key list from file:%s'%restKeyCommand)
                    logger.info('Execute Remote key list from file:%s'%restKeyCommand)
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
                #print('%s function not support!'%(case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]))
                logger.info('%s function not support!'%(case[self.colIdx['Rest_Control']].strip().split(']')[0].split('[')[1]))
        else:
            #print('REST control does not use correctly, please follow the user guide to define the test case!')
            logger.info('REST control does not use correctly, please follow the user guide to define the test case!')


        #RedRat Control Start
        
        if case[self.colIdx['IR_Seq']].strip()!='':
            
            IR_Commands = case[self.colIdx['IR_Seq']].strip().split(']')[1]
            #print("IR Sequence :",IR_Commands)
            logger.info("IR Sequence :",IR_Commands)

            if "RedRat" in case[self.colIdx['IR_Seq']].strip():
                
                RedRat=DEV_REDRAT()
                if '.xml' in IR_Commands:
                    #print("run xml parser")
                    logger.info("run xml parser")
                    Xml_data=XML_PARSE()
                    IR_Macro= Xml_data.Parameter(IR_Commands.strip().split(':')[0],IR_Commands.strip().split(':')[1])
                    #print("IR sequence:",IR_Macro)
                    logger.info("IR sequence:",IR_Macro)
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

            elif "NetRat" in case[self.colIdx['IR_Seq']].strip():
                #print('Send keys by NetRat!')
                logger.info('Send keys by NetRat!')
                NetRat_Control=netIRControl()
                
                if ":" in IR_Commands:
                    
                    #print('Read the IR key sequence for file in testsuite')
                    logger.info('Read the IR key sequence for file in testsuite')
                    NetRat_CaseFolder=IR_Commands.strip().split(':')[0]
                    NetRat_CaseName=IR_Commands.strip().split(':')[1]
                    #print('Case Folder:',NetRat_CaseFolder)
                    logger.info('Case Folder:',NetRat_CaseFolder)
                    #print('Case Name:',NetRat_CaseName)
                    logger.info('Case Name:',NetRat_CaseName)
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

        if case[self.colIdx['SerialCmd']].strip()!='':
            
            ser_cmd_list = case[self.colIdx['SerialCmd']].strip().split(';')

            ser_cmd_index = 0
            #print(len(ser_cmd_list))
            logger.info(len(ser_cmd_list))
            while ser_cmd_index < len(ser_cmd_list):
                #print('Execute the serial command:',ser_cmd_list[ser_cmd_index])
                logger.info('Execute the serial command:',ser_cmd_list[ser_cmd_index])
                self.my_serial.writes(ser_cmd_list[ser_cmd_index].encode('utf-8'))
                time.sleep(float(ser_cmd_list[ser_cmd_index+1]))
                ser_cmd_index = ser_cmd_index+2

        #self.my_serial.write('reboot'.encode('utf-8'))                                 
        
        # Pattern Generator Control 
        # Quantum Data 780, 980 and AstroVG859 could be controled by typical word "VG859","QD780" and "QD980" in test case

        if case[self.colIdx['Device_Control']].strip()!='':
            devCommand=case[self.colIdx['Device_Control']].strip().split(']')[1]
            #print("The device command for QD or Astro or EPCR3::",devCommand)
            logger.info("The device command for QD or Astro or EPCR3::",devCommand)

            if 'VG859' in case[self.colIdx['Device_Control']].strip():
                cfgList = ''
               
                try:            
                    with open(AutoTestAppINI, 'r') as f:
                        cfgList = [line.strip() for line in f.readlines()]
                        ##print cfgList
                        f.close()
                except Exception as e:
                    self.Log(str(e.args))
                
                for item in cfgList:
                    if item.startswith('VG859_IP'):
                        VG859_ip=item.split("=")[1]
                        #print("VG859 IP address:",VG859_ip)
                        logger.info("VG859 IP address:",VG859_ip)

                vg859_timing=devCommand.split(',')[0]
                vg859_pattern=devCommand.split(',')[1]
                #print("VG859 timing and pattern",vg859_timing,vg859_pattern)
                logger.info("VG859 timing and pattern",vg859_timing,vg859_pattern)
                #print('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_timing)
                logger.info('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_timing)
                #print('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_pattern)
                logger.info('.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_pattern)

                subprocess.Popen( '.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_timing,shell=True)
                subprocess.Popen( '.\VG859\VG859LAN-argv.exe '+VG859_ip+' -'+vg859_pattern,shell=True)
                time.sleep(3)
                        
            elif 'QD780' in case[self.colIdx['Device_Control']].strip():    
                qd780_timing = devCommand.split(',')[0]
                qd780_pattern = devCommand.split(',')[1]
                qd780_signaltype = devCommand.split(',')[2]
                qd780_samplemode = devCommand.split(',')[3]
                qd780_bitdepth = devCommand.split(',')[4]

                self.qd_serial.writes(qd780_timing.encode('utf-8'))
                self.qd_serial.writes(qd780_pattern.encode('utf-8'))
                self.qd_serial.writes(qd780_signaltype.encode('utf-8'))
                self.qd_serial.writes(qd780_samplemode.encode('utf-8'))
                self.qd_serial.writes(qd780_bitdepth.encode('utf-8'))
                self.qd_serial.writes('ALLU' + '\n')
                time.sleep(3)
                #print('QuantumData Timing:',qd780_timing)
                #print('QuantumData Pattern:',qd780_pattern)
                #print('QuantumData signaltype:',qd780_signaltype)
                #print('QuantumData samplemode:',qd780_samplemode)
                #print('QuantumData bitdepth:',qd780_bitdepth)

                logger.info('QuantumData Timing:', qd780_timing)
                logger.info('QuantumData Pattern:', qd780_pattern)
                logger.info('QuantumData signaltype:', qd780_signaltype)
                logger.info('QuantumData samplemode:', qd780_samplemode)
                logger.info('QuantumData bitdepth:', qd780_bitdepth)
                
            

                #use my_qd_generator class, need open/close serial everytime.
                #QD_Pattern_Gen=DEV_QD_GEN()
                #QD_Pattern_Gen.QD_Write(pattern)
            elif 'QD980' in case[self.colIdx['Device_Control']].strip():
                QD980 = Telnet_QD980()
                qd980_timing = devCommand.split(',')[0]
                qd980_pattern = devCommand.split(',')[1]
                qd980_signaltype = devCommand.split(',')[2]
                qd980_samplemode = devCommand.split(',')[3]
                qd980_bitdepth = devCommand.split(',')[4]                
                             
                QD980.do_telnet(qd980_timing,qd980_pattern,qd980_signaltype,qd980_samplemode,qd980_bitdepth)
                time.sleep(5)
                
                #print('QuantumData Timing:',qd980_timing)
                #print('QuantumData Pattern:',qd980_pattern)
                #print('QuantumData signaltype:',qd980_signaltype)
                #print('QuantumData samplemode:',qd980_samplemode)
                #print('QuantumData bitdepth:',qd980_bitdepth)                
                #print("qd980 finished")

                logger.info('QuantumData Timing:', qd980_timing)
                logger.info('QuantumData Pattern:', qd980_pattern)
                logger.info('QuantumData signaltype:', qd980_signaltype)
                logger.info('QuantumData samplemode:', qd980_samplemode)
                logger.info('QuantumData bitdepth:', qd980_bitdepth)
                logger.info("qd980 finished")
           
            elif 'EPCR3' in case[self.colIdx['Device_Control']].strip():
                EPCR3 = PowerController()
                epcr3_port = devCommand.split(',')[0]
                epcr3_status = devCommand.split(',')[1]
                #print(("Outlet:" + epcr3_port))
                logger.info(("Outlet:" + epcr3_port))
                #print(("Status:" + epcr3_status))
                logger.info(("Status:" + epcr3_status))
                EPCR3.control_power(epcr3_port,epcr3_status)
                time.sleep(10)
                #print("EPCR3 finished")   
                logger.info("EPCR3 finished")

            elif 'ALISTREAMER' in case[self.colIdx['Device_Control']].strip():
                aliStreamer = AliSteamerPlayer()
                streamName = devCommand.split(',')[0]
                freq = devCommand.split(',')[1]
                streamLoopTimes = devCommand.split(',')[2]
                #print("Alitronika Streamer Settings: StreamName- %s Frequency-%s PlaybackLoopTimes-%s"%(streamName,freq,streamLoopTimes))
                logger.info("Alitronika Streamer Settings: StreamName- %s Frequency-%s PlaybackLoopTimes-%s"%(streamName,freq,streamLoopTimes))
                aliStreamer.Ali_DTV_Player(streamName,freq,streamLoopTimes)

        
        # Image Capture Start      
        
        '''
        capFileName =''
        capTime=0  
        videoPath='.\\Video\\'
        '''
    
        if case[self.colIdx['PIC_Capture']].strip()!='':
            '''
            cap = CameraCapture()
            
            # get the capture file name
            capFileName = case[self.colIdx['PIC_Capture']].strip().split(']')[1].split(',')[0]
            capTime = case[self.colIdx['PIC_Capture']].strip().split(']')[1].split(',')[1] 
            capDir=videoPath+capFileName
            '''
            
            # select the capture device accoriding to the typical word in PIC_Capture column of test case
            # VX1-IMG with Unigraf UCD-2, CAM-IMG with camera for picture, CAM-VIDEO with camera for video
            if 'VX1-IMG' in case[self.colIdx['PIC_Capture']].strip():
               
                
                #E01_SimpleCapture is UCD-2 simple capture program
                subprocess.call('E01_SimpleCapture.exe '+capFileName+' >>./Logs/UCD_log.txt',shell=True)
                
            elif 'CAM-IMG' in case[self.colIdx['PIC_Capture']].strip():
                cap = CameraCapture()
                cap.open()
                cap.imageCapture(capDir+strIMStime,int(capTime))
                cap.close()
                
            elif 'CAM-VIDEO-END' in case[self.colIdx['PIC_Capture']].strip():
                
                # Capture video with OpenCV w/o audio.
                cap.open()
                # caputure video name and time(s) are divided with ","
                cap.videoCapture(capDir+strIMStime,capTime)
                cap.close() 
                
                # Capture Video with FFmpeg Recoder
                #ffmpegCap.ffmpeg_video_record(CameraVDN,CameraADN,capDir+strIMStime+'.mkv',capTime,'"'+case[self.colIdx['Case_ID']].strip()+' '+case[self.colIdx['Case_Description']].strip()+'"')

        #Test Result Ajudgement
        
        ### show Test Result in Table
        Rows = sorted(self.table.GetSelectedRowsFromTable())
        #print('%s rows are selected for testing'%(len(Rows)))
        logger.info('%s rows are selected for testing'%(len(Rows)))

        #Rest/UART Log Info comparision
        if case[self.colIdx['Log_Ref']].strip()!='':
            if case[self.colIdx['Log_Capture']].strip()!='':
                
                #Rest Info comparision
                if case[self.colIdx['Log_Capture']].strip().split(']')[0].split('[')[1]=='REST':
                    restGet = restterminal()
                    restGetCommand=case[self.colIdx['Log_Capture']].strip().split(']')[1]
                    #print('REST Put Command Command:',restGetCommand)
                    logger.info('REST Put Command Command:',restGetCommand)

                    fr=open(Auth_Token, "r")
                    self.read_auth_token=fr.readline().strip('\n')
                    fr.close()
                 
                    restGet.read_dictionary()                             
                    #requests.packages.urllib3.disable_warnings()
                    restGetValue=restGet.parse_command(restGetCommand,self.read_auth_token)
                    #print('Rest Get Value:%s'%restGetValue)
                    logger.info('Rest Get Value:%s'%restGetValue)
                    restGet.parse_command("restlog",self.read_auth_token)
                        
                    if case[self.colIdx['Log_Ref']].strip()==restGetValue:
                        #print("Compare the Rest Log") 
                        logger.info("Compare the Rest Log")
                        case[self.colIdx['Log_Result']]="Pass"
                    
                    else:
                        case[self.colIdx['Log_Result']]="Fail"
                
                #UART Infor Comparision        
                elif case[self.colIdx['Log_Capture']].strip().split(']')[0].split('[')[1]=='UART':
                    #print("reserved")
                    logger.info("reserved")

                else:
                    #print('Please check if test case format for log capture is correct!')
                    logger.info('Please check if test case format for log capture is correct!')

        # Image comparision Start            
        if case[self.colIdx['PIC_Ref']].strip()!='':
            Rows = sorted(self.table.GetSelectedRowsFromTable())
            ref_image=case[self.colIdx['PIC_Ref']].strip()+'.jpg'
            dst_image=capFileName+'.jpg'
            #dst_image='INPUT_002.jpg'
            #print("The reference image name:",ref_image)
            #print("The destination image name:",dst_image)

            logger.info("The reference image name:", ref_image)
            logger.info("The destination image name:", dst_image)
        
            myMatchImage=ImageMatch()
            self.PIC_result=myMatchImage.match(ref_image,dst_image,mode="ahash",win_size=32)
            #print("Result: ham %d\t%s\t%s" % (self.PIC_result, ref_image, dst_image))     
            logger.info("Result: ham %d\t%s\t%s" % (self.PIC_result, ref_image, dst_image))

            if self.PIC_result <=5:
                case[self.colIdx['PIC_Result']]= str(self.PIC_result)+',Pass'
                #print(case[self.colIdx['PIC_Result']])
                logger.info(case[self.colIdx['PIC_Result']])
            else:
                case[self.colIdx['PIC_Result']]= str(self.PIC_result)+',Fail'
                #print(case[self.colIdx['PIC_Result']])   
                logger.info(case[self.colIdx['PIC_Result']])

        #Audio Comparision Start
        if case[self.colIdx['Audio_Ref']].strip()!='':
            #print("reserved")
            logger.info("reserved")

        #Write the result in selected Table        
        if self.rowNumber < len(Rows):
            ##print "cherry temp log2:",Rows[0]
            #print("Total:",Rows[self.rowNumber])
            logger.info("Total:{}".format(Rows[self.rowNumber]))
            #print("Cases Info:",case)
            logger.info("Cases Info:{}".format(case))
            self.table.SetRowValueToTable(Rows[self.rowNumber],case)
        
        #Close camera
        #cap.close()   
        
        ret = 0        
        
        # Show the execute result
        t = time.localtime(time.time())
        strIMSt = time.strftime("%I:%M:%S", t)
        #self.testcase.AppendText(strIMSt +' Result: ' + str(ret)+"\n\n")
        
        
        
    def OnRunCase(self,event):
        global case
        self.rowNumber = 0
        Rows = sorted(self.table.GetSelectedRowsFromTable())
        try:        
            case = self.table.GetRowValueFromTable(Rows[0])
        except Exception as e:
            self.Log(str(e.args))

        #self.Log( "case avail %s %s" % ( str(case[self.colIdx['Available']]), str(type(case[self.colIdx['Available']]))))
        if case[self.colIdx['Available']] == '' or int(case[self.colIdx['Available']]) == 0:
            dlg = wx.MessageDialog(self, "The case is not available",
                                      'Message',style=wx.OK)
            dlg.ShowModal()  
            dlg.Destroy()
            return            
        
        try:
            self.RunCase(case)
        except Exception as e:
            self.Log( "Error: %s" % str(e.args) )
            pass

        
    def OnNextCase(self,event):
        self.table.MoveToNextRow()
        Rows = sorted(self.table.GetSelectedRowsFromTable())
        try:        
            case = self.table.GetRowValueFromTable(Rows[0])
        except Exception as e:
            self.Log(str(e.args))
            
        self.log( 'Next--> %s' % case )
        
    def OnStopCurrCase(self, event):
        self.Log('Stop Current Case')
        self.StopPrevCase()
               
    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""
            
    def AddCaseToTable(self, source_name, case):
        for idx in self.df.index:
            if source_name in self.df.loc[idx,'Category']:
                if case in self.df.loc[idx, 'Case_ID']:
                    #row = list(self.df.loc[idx,:'Case_ID']) +list(self.df.loc[idx,'Case_Available':])
                    row = list(self.df.loc[idx,'Category':])
                    for i in range(len(row)):
                        try:
                            if math.isnan(row[i]):
                                row[i] = ''
                        except Exception as e:
                            pass
                    #print(row)
                    logger.info(row)
                    self.Log(str(row))
                    self.table.AppendRowsToTable([row])
        
    def OnTreeActivated(self, evt):
        self.Log( "\n\nOnActivated:    %s" % str(self.GetItemText(evt.GetItem())))
        
        # only to activate the stream name(root's children) take effect
        item = evt.GetItem()
        root = self.tree.GetRootItem()
        if self.tree.GetItemParent(item) == root:
            # source is activated
            source_name = self.GetItemText(item)    
            for case in self.sources[source_name]:
                self.AddCaseToTable(source_name, case)
        elif item != root:
            # only the case is activated
            source_name = self.GetItemText(self.tree.GetItemParent(item))   
            case = self.GetItemText(item)
            self.AddCaseToTable(source_name, case)
                            
        self.table.AutoSizeColumns(True)   

    def OnDeleteRows(self, event):
        Rows = sorted(self.table.GetSelectedRowsFromTable(), reverse=True) 
        for pos in Rows:
            self.table.DeleteRowsFromTable(pos, numRows=1)
            self.Log( "delete Row: %s" % str(pos))
        self.table.AutoSizeColumns(True) 
        self.Log( "Rows: %s" % str(Rows))

    def RedRatRunRows(self, event):
        self.RedRat.run()

    def RedRatKillRows(self, event):
        self.RedRat.kill()

    def SettingRunRows(self, event):
        self.Set = SetFileIni()
        self.Set.Show()

    def Onpenvideo(self, event):
        # os.system("explorer %s" % File_Path + "\Video")
        os.startfile(File_Path + "\Video")

    def Onclearvideo(self, event):
        ls = os.listdir(File_Path + "\Video")
        if self.ShowMessage() == wx.ID_YES:
            for i in ls:
                c_path = os.path.join(File_Path + "\Video", i)
                if os.path.isdir(c_path):
                    self.Onclearvideo(c_path)
                else:
                    os.remove(c_path)

    def ShowMessage(self):
        info = wx.MessageDialog(self, "Are you sure you want to delete all videos ?",
                                      'Warning',style=wx.YES_NO|wx.ICON_EXCLAMATION)
        return info.ShowModal()

    def ShowMessage1(self):
        info = wx.MessageDialog(self, "You need to choose case",
                                      'Warning',style=wx.OK|wx.ICON_EXCLAMATION)
        return info.ShowModal()

    def OnExit(self):
        self.StopPrevCase()
        self.serial_stop()
        self.T.kill()
        self.RedRat.kill()
        self.Log( "Destroy Source Window" )
        self.Destroy()
        

class AutoTestAppFrame(wx.Frame):
    def __init__(self, parent, title, log):
        wx.Frame.__init__(self, parent, title=title)

        self.title = None
        self.createMenuBar()
        self.initStatusBar()
        #self.createToolBar()
        
        p = wx.Panel(self)                
        
        self.autotest_app = AutoTestAppPanel(p, log)                 
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.autotest_app,1,flag=wx.EXPAND)
        p.SetSizer(sizer)
        
        self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)
        
   
    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])
    
        
    def menuData(self):
        return [("&File", (
                ("&New", "New testcase file", self.OnNew),
                ("&Open", "Open testcase file", self.OnOpen),
                ("&Save", "Save testcase file", self.OnSave),                
                ("", "", ""),
                ("About...", "Show about window", self.OnAbout),
                ("&Quit", "Quit", self.OnCloseWindow)))]

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

        
    def toolbarData(self):
            return (("New", "new.bmp", "Create new HalSys", self.OnNew),
                    ("", "", "", ""),
                    ("Open", "open.bmp", "Open existing HalSys", self.OnOpen),
                    ("Save", "save.bmp", "Save existing HalSys", self.OnSave))
    
    def createToolBar(self):
        toolbar = self.CreateToolBar()
        for each in self.toolbarData():
            self.createSimpleTool(toolbar, *each)
        toolbar.AddSeparator()        
        toolbar.Realize()
            
    def createSimpleTool(self, toolbar, label, filename, help, handler):
        if not label:
            toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def OnNew(self, event): pass
    
    wildcard = "Config files (*.cfg)|*.cfg|All files (*.*)|*.*"
    
    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Open file...", os.getcwd(),
                           style=wx.FD_OPEN, wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            #self.ReadFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def OnSave(self, event):
        if not self.filename:
            self.OnSaveAs(event)
        else:
            self.SaveFile()

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, "Save as...", os.getcwd(),
                           style=wx.FD_OPEN | wx.FD_OVERWRITE_PROMPT,
                           wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.HalSys'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()
    '''
    def OnSetPos(self, evt):
        initpos = wx.GetNumberFromUser(
            "Enter the initial sash position (to be used in the Split call)",
            "", "Initial Sash Position", self.initpos,
            -1000, 1000, self)
        if initpos != -1:
            self.initpos = initpos
    '''
    
    def OnCloseWindow(self, event):
        #print("Before Destroy main")
        logger.info("Before Destroy main")
        self.autotest_app.OnExit()
        self.Destroy()    

    def OnExit(self, evt):
        #print("Before Close main")
        logger.info("Before Close main")
        self.Close()

    def OnAbout(self, event):
        dlg = VsiliconAbout(None)
        dlg.ShowModal()
        dlg.Destroy()

    def SaveFile(self):
        pass

class AutoTestApp(wx.App):
    @profile
    def OnInit(self):

        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        #splash screen
        bmp = wx.Image(".\\icons\\v-logo.jpg",wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wx.adv.SplashScreen(bmp, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                1000, None, -1)
        wx.Yield()
        time.sleep(3)

        frame = AutoTestAppFrame(None, "V-Silicon AutoTestApp v2.2.0", sys.stdout)
        icon = wx.Icon(name=".\\icons\\V.ico",type=wx.BITMAP_TYPE_ICO)
        frame.SetIcon(icon)
        frame.tbicon=wx.adv.TaskBarIcon()
        frame.tbicon.SetIcon(icon)
        frame.SetSize((800,600))
        self.SetTopWindow(frame)
        frame.Show(True)

        return True

if __name__ == '__main__':
    app = AutoTestApp(False,'caplog')
    app.MainLoop()

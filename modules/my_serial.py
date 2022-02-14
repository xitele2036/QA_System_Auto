# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:16:13 2018

@author: yongsongzhu
"""

# -*- coding: utf-8 -*-

import wx
import sys
#import time
import threading
import time
import serial
import serial.tools.list_ports
import copy


import wx.lib.buttons as buttons

class SigmaSerial(object):
    def __init__(self):
        self.my_serial = None
        self.port_name_list = []  
        self.port_name = ''
        self.autodetect()
    
    def isOpen(self):        
        if not self.my_serial is None:
            return self.my_serial.isOpen()
        else:
            return False
    
    def open(self, port_name=None, baudrate=115200):
        
        if not self.my_serial is None:
            if self.my_serial.isOpen():
                print("Serial has been started, stop it firstly\n")
                self.my_serial.close()
                
        if port_name is None:
            if len(self.port_name_list) == 0:
                self.autodetect()
            self.port_name = self.port_name_list[0]            
        else:
            self.port_name = port_name
            
        if not self.port_name.startswith('COM'):
            print('Port name is wrong', self.port_name)
            return False
            
        self.my_serial = serial.Serial()
        self.my_serial.port= self.port_name        
        self.my_serial.baudrate = baudrate
        self.my_serial.bytesize=serial.EIGHTBITS
        self.my_serial.parity=serial.PARITY_NONE
        self.my_serial.stopbits=serial.STOPBITS_ONE
        self.my_serial.open()
        if self.my_serial.isOpen(): 
            return True
        else:
            return False
    
    def readlines(self):
        try:
            if self.my_serial.isOpen():                
                return self.my_serial.readline().decode('UTF-8')
        except Exception as ex:
            print (ex)
        
        return ''
    
    def writes(self, cmd, *args, **kw):
        '''
        args = ('a', 'b')
        kw = {'dict':99}
        '''
        msg = copy.deepcopy(cmd)
        for i in range(len(args)):
            msg += ' ' + args[i]
            
        print("Write Cmd:",msg)
        
        # return self.my_serial.write(msg + '\n')
        return self.my_serial.write(msg.encode() + b'\n')
        # return self.my_serial.write(msg.encode('UTF-8') + '\n')
        # return self.my_serial.write(msg.encode('UTF-8') + '\n')

    def close(self):
        if self.my_serial.isOpen():
            self.my_serial.close()
    
    def autodetect(self):
        serial_list = list(serial.tools.list_ports.comports())
        #print serial_list
        if serial_list:	
            self.port_name_list = []			
            for i in range(0, len(serial_list)):
                portname = list(serial_list[i])
                self.port_name_list.append(str(portname[0]))
            print("Available serial port list: ", self.port_name_list)

class MySerialFrame(wx.Panel):
    def __init__(self, parent, log):
        
        self.local = wx.Locale(wx.LANGUAGE_CHINESE_SIMPLIFIED)
                
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        
        self.my_serial = None
        self.alive = False
        #self.waitEnd = None        
        self.thread_read = None
        self.portlist = None
              
        """
        #############   Left Layout
        """  
              
        label1 = wx.StaticText(self, -1, "Port")
        #self.port = wx.TextCtrl(self, -1, '')    
        self.portlist = wx.ComboBox(self, -1, pos=wx.Point(10,100), size=wx.Size(100,50), style=wx.CB_READONLY)
        #self.portlist.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.evt_combox_dropdown)

        label2 = wx.StaticText(self, -1, "BaudRate")
        self.baudrate = wx.TextCtrl(self, -1, '115200')
        self.connect = buttons.GenToggleButton(self, -1, "Connect...")
        self.Bind(wx.EVT_BUTTON, self.OnConnect, self.connect)
        self.connect.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        self.connect.SetBezelWidth(2)
        
        leftSizer = wx.BoxSizer(wx.VERTICAL)        
        leftSizer.Add(label1, 0, wx.EXPAND|wx.ALL,5) 
        leftSizer.Add(self.portlist, 0, wx.EXPAND|wx.ALL,5)
        leftSizer.Add(label2, 0, wx.EXPAND|wx.ALL,5) 
        leftSizer.Add(self.baudrate, 0, wx.EXPAND|wx.ALL,5)
        leftSizer.Add(self.connect, 0, wx.EXPAND|wx.ALL,5)
        
        
        #--------------------------------------------------------------
        
        
        label3 = wx.StaticText(self, -1, "Message")
        self.show = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)

        self.command = wx.TextCtrl(self, -1, '')        
        self.send = wx.Button(self, -1, "Send")
        self.Bind(wx.EVT_BUTTON, self.OnSendCommand, self.send)
        
        msgSizer = wx.BoxSizer(wx.VERTICAL)        
        msgSizer.Add(label3, 0, wx.EXPAND|wx.ALL,5) 
        msgSizer.Add(self.show, 4, wx.EXPAND|wx.ALL,5)
        
        cmdSizer = wx.BoxSizer(wx.HORIZONTAL)        
        cmdSizer.Add(self.command, 4, wx.EXPAND|wx.ALL,5) 
        cmdSizer.Add(self.send, 1, wx.EXPAND|wx.ALL,5)            
        
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(msgSizer, 4, wx.EXPAND|wx.ALL,5) 
        rightSizer.Add(cmdSizer, 1, wx.EXPAND|wx.ALL,5)
       
        
        """
        #############  Whole Layout
        """
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(leftSizer, 1, wx.EXPAND|wx.ALL, 5)                
        mainSizer.Add(rightSizer, 4, wx.EXPAND|wx.ALL, 5)               
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        #mainSizer.SetSizeHints(self) 
        
        # EVT_CLOSE is not triggerred, which only is triggered in the top window
        #self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)
        
        self.my_serial = SigmaSerial()
        self.portlist.SetItems(self.my_serial.port_name_list)
        
    def Log(self, msg):
        self.show.AppendText(msg+"\n")
        
        
    def OnConnect(self, event):
        if self.portlist is None:
            self.DetectSerialPort()
            
        button = event.GetEventObject()
        if button.GetValue():
            self.start()
            if not self.my_serial.isOpen():
                button.SetLabel("Fail,TryAgain")                    
            else:             
                button.SetLabel("Disconnect")  
            
            #button.SetFocus()
            button.Refresh()
        else:
            self.stop()
            button.SetLabel("Connect...")            
            #button.SetBackgroundColour("Red")
            
        event.Skip()   
        
    def OnSendCommand(self, event):
        if self.alive:
            # try:
                snddata=self.command.GetValue()
                self.my_serial.writes(snddata)
                self.show.AppendText('#' + snddata+'\n') 
                print('SEND CMD: '+' '+ time.strftime("%Y-%m-%d %X") + ' ' + snddata)
                
            # except Exception as ex:
            #     print (ex)
        event.Skip()
    '''    
    def waiting(self):
        # wait for event stop flag
        if not self.waitEnd is None:
            self.waitEnd.wait()
    '''
        
    def start(self): 
                
        try:            
            self.my_serial.open()
                 
            if self.my_serial.isOpen():
                #self.waitEnd = threading.Event()
                self.alive = True
                
                self.thread_read = threading.Thread(target=self.Reader)
                self.thread_read.setDaemon(True)
                
                self.thread_read.start()
                return True
            else:
                print('Serial has not been started\n')
                return False
        except Exception as ex:
            print (ex)
            return False        
            
    def Reader(self):
        while self.alive:
            try:
                '''
                n=self.my_serial.inWaiting()
                data=''
                if n:
                    data= self.my_serial.read(n).decode('utf-8')             
                    #print ('recv'+' '+time.strftime("%Y-%m-%d %X")+' '+data.strip())
                    #print (time.strftime("%Y-%m-%d %X:")+data.strip(),file=self.rfile)
                    self.show.AppendText(data.strip()+'\n')
                    if len(data)==1 and ord(data[len(data)-1])==113: #收到字母q，程序退出
                        break
                '''
                data = self.my_serial.readlines().decode('UTF-8')
                if len(data) > 1:
                    self.show.AppendText(data.strip()+'\n') 
            except Exception as ex:
                print (ex)
 
        #self.waitEnd.set()
        self.alive = False
    
    def searchstr(self,keyWord):
        if self.alive:
            try:
                f=open('log.txt')
                line=f.readlines()
                linen=1
                while line:
                    if not line.find(keyWord)==-1:
                        linen+=1
                        line=f.readlines()
                    else:
                        print('KeyWork was found')    
                f.close()
            except Exception as ex:
                print (ex)    

    def stop(self):
        self.alive = False
        #self.thread_read.join()
        #self.thread_send.join()
        if self.my_serial.isOpen():
            self.my_serial.close()
       
   
    def OnExit(self):
        self.stop()
        self.Destroy()
        print("Destroy Window")
        

class SerialFrame(wx.Frame):
    def __init__(self, parent, title, log):
        wx.Frame.__init__(self, parent, title=title)
        
        p = wx.Panel(self)                
        
        self.serial_app = MySerialFrame(p, log)                 
        
        sizer=wx.BoxSizer(wx.VERTICAL)        
        sizer.Add(self.serial_app,1,flag=wx.EXPAND)
        p.SetSizer(sizer)
        
        self.Bind(wx.EVT_CLOSE,  self.OnCloseWindow)  
  
    def OnCloseWindow(self, event):        
        self.Destroy()    

    def OnExit(self, evt):
        self.Close()


class SerialApp(wx.App):

    def OnInit(self):        
        #bmp = wx.Image("startup1.jpg").ConvertToBitmap()
        #wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
        #        1000, None, -1)
        #wx.Yield()
        
        frame = SerialFrame(None, "Serial App", sys.stdout) #HalSysFrame(None)
        frame.SetSize((800,600))
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = SerialApp(False)
    app.MainLoop()

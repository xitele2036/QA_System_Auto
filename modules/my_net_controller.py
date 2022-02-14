import sys
import requests
import json
from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageTk
import threading
import queue
import subprocess
import time
import os
import shutil
import socket
from modules.TestCfgParse import TestCfgParse,CfgParse


log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__))+'/Config')
AutoTestAppINI = log_file_path + '/AutoTestApp.INI'

restCfg = CfgParse(AutoTestAppINI)
IP = restCfg.GetCfgInfo("RestConnection","Ethernet.IP") #DUT IP Address
print(("DUT IP address:",IP))
PORT=restCfg.GetCfgInfo("RestConnection","Port") # REST Port
print(("REST Port:",PORT))
UDP_PORT=restCfg.GetCfgInfo("RestConnection","UDP_PORT") # REST Port
print(("UDP Port:",UDP_PORT))
DICT_FILE=restCfg.GetCfgInfo("RestConnection","DICT_FILE") # Rest Dictionary
print(("Dictionary File:",DICT_FILE))

UseRest = 1
#IP = "10.86.78.46"
#PORT = "7345"
#UDP_PORT = 54321
DEVICE_NAME = "TABLET"
DEVICE_ID = "1234567890"
HEADERS = {"Content-Type": "application/json"}
AUTH_TOKEN = ""
uri = "https://" + IP + ":" + PORT 
suitelevel = 0
caselevel = 1
file_location = suitelevel
INPUT_data = b'\x60\x00\x10\x00\x11'
MENU_data = b'\x60\x00\x10\x00\x0F'
UP_data = b'\x60\x00\x10\x00\x07'
DOWN_data = b'\x60\x00\x10\x00\x06'
LEFT_data = b'\x60\x00\x10\x00\x08'
RIGHT_data = b'\x60\x00\x10\x00\x09'
OK_data = b'\x60\x00\x10\x00\x0B'
EXIT_data = b'\x60\x00\x10\x00\x16'
POWER_data = b'\x60\x00\x10\x00\x17'
BACK_data = b'\x60\x00\x10\x00\x0E'
INFO_data = b'\x60\x00\x10\x00\x2B'
CHUP_data = b'\x60\x00\x10\x00\x12'
CHDOWN_data = b'\x60\x00\x10\x00\x13'
VOLUP_data = b'\x60\x00\x10\x00\x14'
VOLDOWN_data = b'\x60\x00\x10\x00\x15'
MUTE_data=b'\x60\x00\x10\x00\x18'
ONE_data = b'\x60\x00\x10\x00\x19'
TWO_data = b'\x60\x00\x10\x00\x1A'
THREE_data = b'\x60\x00\x10\x00\x1B'
FOUR_data = b'\x60\x00\x10\x00\x1C'
FIVE_data = b'\x60\x00\x10\x00\x1D'
SIX_data = b'\x60\x00\x10\x00\x1E'
SEVEN_data = b'\x60\x00\x10\x00\x1F'
EIGHT_data = b'\x60\x00\x10\x00\x20'
NINE_data = b'\x60\x00\x10\x00\x21'
ZERO_data = b'\x60\x00\x10\x00\x22'

PLAY_data = b'\x60\x00\x10\x00\x0C'
PAUSE_data = b'\x60\x00\x10\x00\x0D'
PREV_data = b'\x60\x00\x10\x00\x40'
NEXT_data = b'\x60\x00\x10\x00\x41'
STOP_data = b'\x60\x00\x10\x00\x5E'
BACKWARD_data = b'\x60\x00\x10\x00\x42'
FORWARD_data = b'\x60\x00\x10\x00\x43'
CC_data=b'\x60\x00\x10\x00\x10'

WIDE_data=b'\x60\x00\x10\x00\x39'
LAST_data=b'\x60\x00\x10\x00\x0D'
GUIDE_data=b'\x60\x00\x10\x00\x25'
PIC_data = b'\x60\x00\x10\x00\x7F'
ENTER_data = b'\x60\x00\x10\x00\x61'

#OTT short keys
VIA_data = b'\x60\x00\x10\x00\x28'
AMAZON_data = b'\x60\x00\x10\x00\x84'
NETFLIX_data = b'\x60\x00\x10\x00\x85'
VUDU_data = b'\x60\x00\x10\x00\x86'
MGO_data = b'\x60\x00\x10\x00\x87'
IHEART_data = b'\x60\x00\x10\x00\x88'
HULU_data = b'\x60\x00\x10\x00\x90'
CRACKLE_data = b'\x60\x00\x10\x00\x91'
PLUTO_data = b'\x60\x00\x10\x00\x92'
YOUTUBE_data = b'\x60\x00\x10\x00\x93'
XUMO_data = b'\x60\x00\x10\x00\x94'
SLING_data = b'\x60\x00\x10\x00\x95'
WatchFree_data = b'\x60\x00\x10\x00\x98'



class AsynchronousFileReader(threading.Thread):
    def __init__(self, fd, reader_queue):
        assert isinstance(reader_queue, queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = reader_queue

    def run(self):
        for lines in iter(self._fd.readline, ''):
            self._queue.put(lines)

    def eof(self):
        return not self.is_alive() and self._queue.empty()

def get_authtoken():
    global IP
    global HEADERS
    global PORT
    
    subprocess.call(["adb", "disconnect"])
    subprocess.call(["adb", "connect", IP])
    process = subprocess.Popen(["adb", "shell", "logcat"], stdout=subprocess.PIPE)
    stdout_queue = queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    
    uri = "https://" + IP + ":" + PORT + "/pairing/start"
    payload = json.dumps({"DEVICE_ID": DEVICE_ID, "DEVICE_NAME": DEVICE_NAME})
    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
    print(result)
    if result["STATUS"]["RESULT"] != "SUCCESS":
        print(("Can't connect to TV. STATUS: %s" % result["STATUS"]["RESULT"]))
        exit(1)

    challenge_type = result["ITEM"]["CHALLENGE_TYPE"]
    req_token = result["ITEM"]["PAIRING_REQ_TOKEN"]
# find challenge pin and check if it gives a valid authentication token
    while not stdout_reader.eof():
        while not stdout_queue.empty():
            line = stdout_queue.get().decode("utf-8", errors="ignore")
            if "PingCode" in line:
                trash, line = line.split("PingCode", 1)
                pins = line.split()
                challenge_pin = pins[0]
                if(len(challenge_pin)!=4):
                    challenge_pin = challenge_pin[:4]                
                print(("pincode="+challenge_pin))

                uri = "https://" + IP + ":" + PORT + "/pairing/pair"
                payload = json.dumps({"DEVICE_ID": DEVICE_ID, "CHALLENGE_TYPE": challenge_type,"RESPONSE_VALUE": challenge_pin, "PAIRING_REQ_TOKEN": req_token})
                print(payload)                
                result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
            
                if(result["STATUS"]["RESULT"] == "SUCCESS"):
                    AUTH_TOKEN=result["ITEM"]["AUTH_TOKEN"]
                    subprocess.call(["adb", "disconnect"])
                    process.stdout.close()

                    fau= open("authtoken.log","w")
                    fau.write(AUTH_TOKEN)
                    fau.close()
                    return AUTH_TOKEN

def send_data(senddata, action):
    global start_time
    global end_time
    
    print("send key to IP",IP)
    print("send key to UDP Port",UDP_PORT)

    end_time = time.time()
    time_taken = abs(start_time - end_time)
    print(senddata)
    print(action)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    print((socket.gethostbyname(socket.getfqdn())))	
    sock.bind((socket.gethostbyname(socket.getfqdn()), int(UDP_PORT)))	
    sock.sendto(senddata, (IP, int(UDP_PORT)))
    sock.close()
    if recordflag == 1:
        if time_taken < 0.3:
            time_taken = 0.3
        fw.write("sleep "+str(time_taken)+"\n")
        fw.write(action+"\n")    
    start_time = time.time()

def netIR_send_data(senddata, action):

    print(senddata)
    print(action)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    print((socket.gethostbyname(socket.getfqdn())))	
    sock.bind((socket.gethostbyname(socket.getfqdn()), int(UDP_PORT)))	
    sock.sendto(senddata, (IP, int(UDP_PORT)))	

class netIRControl(object):
	       
        
    def autoplaycase(self,suite_name,case_name):

        print('test start:')
        print(("playcase:", case_name))
        print((suite_name+'/'+case_name))    
        shutil.copy2(suite_name +'/' + case_name, '../execute.txt')
        self.say_playonce()  
        
    def say_hi(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":7,"CODE":5,"ACTION":"KEYPRESS"}]})
        #button_action("INPUT")
        netIR_send_data(INPUT_data, "INPUT")	
        
    def say_playonce(self):
        with open('../execute.txt') as f:
            for line in f:
                print (line)
                if 'sleep' in line:
                    sleeptime=line[6:]
                    print(sleeptime)          
                    time.sleep(float(sleeptime))
                else:
                    #subprocess.call("bash control.sh "+line)
                    if 'INPUT' in line:
                        self.say_hi()
                    elif 'MENU' in line:
                        self.say_menu()
                    elif 'EXIT' in line:
                        self.say_exit()
                    elif 'BACK' in line:
                        self.say_back()
                    elif 'INFO' in line:
                        self.say_info()
                    elif 'POWER' in line:
                        self.say_power()
                    elif 'OK' in line:
                        self.say_ok()
                    elif 'LEFT' in line:
                        self.say_left()
                    elif 'RIGHT' in line:
                        self.say_right()
                    elif 'UP' in line:
                        self.say_up()
                    elif 'DOWN' in line:
                        self.say_down()
                    elif 'CC' in line:
                        self.say_CC()
                    elif 'PIC_MODE' in line:
                        self.say_pic()
                    elif 'WIDE' in line:
                        self.say_wide()
                    elif 'VOLUP' in line:
                        self.say_volplus()
                    elif 'VOLDOWN' in line:
                        self.say_volmins()
                    elif 'MUTE' in line:
                        self.say_mute()                    
                    elif 'CHUP' in line:
                        self.say_chplus()
                    elif 'CHDOWN' in line:
                        self.say_chmins()
                    elif 'VIA' in line:
                        self.say_vizio()
                    elif 'vudu' in line:
                        self.say_vudu()
                    elif 'netflix' in line:
                        self.say_netflix()
                    elif 'amazon' in line:
                        self.say_amazon()
                    elif 'xumo' in line:
                        self.say_xumo()
                    elif 'crackle' in line:
                        self.say_crackle()
                    elif 'iheart' in line:
                        self.say_iheart()
                    elif 'watchfree' in line:
                        self.say_watchfree()                    
                    elif '1' in line:
                        self.say_1()
                    elif '2' in line:
                        self.say_2()
                    elif '3' in line:
                        self.say_3()
                    elif '4' in line:
                        self.say_4()
                    elif '5' in line:
                        self.say_5()
                    elif '6' in line:
                        self.say_6()
                    elif '7' in line:
                        self.say_7()
                    elif '8' in line:
                        self.say_8()
                    elif '9' in line:
                        self.say_9()
                    elif '0' in line:
                        self.say_0()  
                        
    def say_playsinglekey(self, IR_key,Pause_time):
        
        if 'INPUT' in IR_key:
            self.say_hi()
        elif 'MENU' in IR_key:
            self.say_menu()
        elif 'EXIT' in IR_key:
            self.say_exit()
        elif 'BACK' in IR_key:
            self.say_back()
        elif 'INFO' in IR_key:
            self.say_info()
        elif 'POWER' in IR_key:
            self.say_power()
        elif 'OK' in IR_key:
            self.say_ok()
        elif 'LEFT' in IR_key:
            self.say_left()
        elif 'RIGHT' in IR_key:
            self.say_right()
        elif 'UP' in IR_key:
            self.say_up()
        elif 'DOWN' in IR_key:
            self.say_down()
        elif 'CC' in IR_key:
            self.say_CC()
        elif 'PIC_MODE' in IR_key:
            self.say_pic()
        elif 'WIDE' in IR_key:
            self.say_wide()
        elif 'VOLUP' in IR_key:
            self.say_volplus()
        elif 'VOLDOWN' in IR_key:
            self.say_volmins()
        elif 'MUTE' in IR_key:
            self.say_mute()
        elif 'CHUP' in IR_key:
            self.say_chplus()
        elif 'CHDOWN' in IR_key:
            self.say_chmins()
        elif 'VIA' in IR_key:
            self.say_vizio()
        elif 'vudu' in IR_key:
            self.say_vudu()
        elif 'netflix' in IR_key:
            self.say_netflix()
        elif 'amazon' in IR_key:
            self.say_amazon()
        elif 'xumo' in IR_key:
            self.say_xumo()
        elif 'crackle' in IR_key:
            self.say_crackle()
        elif 'iheart' in IR_key:
            self.say_iheart()
        elif 'watchfree' in IR_key:
            self.say_watchfree()
        elif '1' in IR_key:
            self.say_1()
        elif '2' in IR_key:
            self.say_2()
        elif '3' in IR_key:
            self.say_3()
        elif '4' in IR_key:
            self.say_4()
        elif '5' in IR_key:
            self.say_5()
        elif '6' in IR_key:
            self.say_6()
        elif '7' in IR_key:
            self.say_7()
        elif '8' in IR_key:
            self.say_8()
        elif '9' in IR_key:
            self.say_9()
        elif '0' in IR_key:
            self.say_0()    
        time.sleep(float(Pause_time))
                        
    def say_exit(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":3,"ACTION":"KEYPRESS"}]})
        #button_action("exit")
        netIR_send_data(EXIT_data, "EXIT")

    def say_power(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":11,"CODE":2,"ACTION":"KEYPRESS"}]})
        #button_action("power")
        netIR_send_data(POWER_data, "POWER")		
        
    def say_vudu(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "8", "MESSAGE": "https://my.vudu.com/castReceiver/index.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 0, "APP_ID": "36346174", "MESSAGE": "{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{\"launchedFromCustomIRButton\": true}}}"}})
        #button_action("vudu")
        netIR_send_data(VUDU_data,"vudu")

    def say_netflix(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 3, "APP_ID": "1", "MESSAGE": "http://127.0.0.1:12345/scfs/sctv/main.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 3, "APP_ID": "1", "MESSAGE": None}})
        #button_action("netflix")
        netIR_send_data(NETFLIX_data,"netflix")

    def say_amazon(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "4", "MESSAGE": "https://atv-ext.amazon.com/blast-app-hosting/html5/index.html?deviceTypeID=A3OI4IHTNZQWDD"}})
        #button_action("amazon")
        netIR_send_data(AMAZON_data,"amazon")

    def say_xumo(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "6", "MESSAGE": "https://vizio-smartcast-app.xumo.com/latest/index.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 0, "APP_ID": "36E1EA1F", "MESSAGE": "{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{}}}"}})
        #button_action("xumo")
        netIR_send_data(XUMO_data,"xumo")

    def say_crackle(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "5", "MESSAGE": "https://crackleott.s3.amazonaws.com/vizio/prod/index.html?cmpid=Vizio_Remote_Launch"}})
        #button_action("crackle")
        netIR_send_data(CRACKLE_data,"crackle")
        

    def say_iheart(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "6", "MESSAGE": "https://tv.iheart.com/smartcast/"}})
        #button_action("iheart")
        netIR_send_data(IHEART_data,"iheart")
        
    def say_watchfree(self):
        netIR_send_data(WatchFree_data,"watchfree")
        
    def say_menu(self):
        #global uri
        #global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":8,"ACTION":"KEYPRESS"}]})
        #button_action("MENU")
        print("...menu")		
        netIR_send_data(MENU_data, "MENU")
        
    def say_mute(self):
        
        print("...mute")		
        netIR_send_data(MUTE_data, "MUTE")    
        
    def say_up(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":8,"ACTION":"KEYPRESS"}]})
        #button_action("up")
        netIR_send_data(UP_data, "UP")		
        
    def say_left(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("left")
        netIR_send_data(LEFT_data, "LEFT")		
        
    def say_right(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":7,"ACTION":"KEYPRESS"}]})
        #button_action("right")
        netIR_send_data(RIGHT_data, "RIGHT")		
        
    def say_down(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("down")
        netIR_send_data(DOWN_data, "DOWN")		
        
    def say_ok(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":2,"ACTION":"KEYPRESS"}]})
        #button_action("ok")
        netIR_send_data(OK_data, "OK")		
        
    def say_back(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("back")
        netIR_send_data(BACK_data, "BACK")		
        
    def say_info(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":6,"ACTION":"KEYPRESS"}]})
        #button_action("info")
        netIR_send_data(INFO_data,"INFO")
        
    def say_CC(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":13,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("CC")
        netIR_send_data(CC_data,"CC")
        
    def say_pic(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":6,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("pic")
        netIR_send_data(PIC_data,"PIC_MODE")
        
    def say_wide(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":6,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("pic")
        netIR_send_data(WIDE_data,"WIDE")    
        
    def say_vizio(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":15,"ACTION":"KEYPRESS"}]})
        #button_action("vizio")
        netIR_send_data(VIA_data,"VIA")
        
    def say_volplus(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":5,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("volplus")
        netIR_send_data(VOLUP_data, "VOLUP")		
        
    def say_volmins(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":5,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("volmins")
        netIR_send_data(VOLDOWN_data, "VOLDOWN")		
        
    def say_chplus(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":8,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("chplus")
        netIR_send_data(CHUP_data, "CHUP")		
        
    def say_chmins(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":8,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("chmins")
        netIR_send_data(CHDOWM_data, "CHDOWN")		
        
    def say_1(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":49,"ACTION":"KEYPRESS"}]})
        #button_action("1")
        netIR_send_data(ONE_data, "1")		
        
    def say_2(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":50,"ACTION":"KEYPRESS"}]})
        #button_action("2")
        netIR_send_data(TWO_data, "2")
        
    def say_3(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":51,"ACTION":"KEYPRESS"}]})
        #button_action("3")
        netIR_send_data(THREE_data, "3")		
        
    def say_4(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":52,"ACTION":"KEYPRESS"}]})
        #button_action("4")
        netIR_send_data(FOUR_data, "4")		
        
    def say_5(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":53,"ACTION":"KEYPRESS"}]})
        #button_action("5")
        netIR_send_data(FIVE_data, "5")		
        
    def say_6(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":54,"ACTION":"KEYPRESS"}]})
        #button_action("6")
        netIR_send_data(SIX_data, "6")		
        
    def say_7(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":55,"ACTION":"KEYPRESS"}]})
        #button_action("7")
        netIR_send_data(SEVEN_data, "7")		
        
    def say_8(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"Csend_data(MENU_data)ODESET":0,"CODE":56,"ACTION":"KEYPRESS"}]})
        #button_action("8")
        netIR_send_data(EIGHT_data, "8")		
        
    def say_9(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":57,"ACTION":"KEYPRESS"}]})
        #button_action("9")
        netIR_send_data(NINE_data, "9")	
    
    def say_0(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":57,"ACTION":"KEYPRESS"}]})
        #button_action("9")
        netIR_send_data(ZERO_data, "0")    		

 
def get_filenames():
    global casename

    path = casename
    return os.listdir(path)

def get_suites():
    #path = "."
    dirs = list(filter(os.path.isdir, os.listdir(os.getcwd())))    
    return dirs
    
def OnDouble(event):
    global casename
    global suitename    
    global file_location
    global listbox
    
    widget = event.widget
    selection=widget.curselection()
    casename = widget.get(selection[0])
    if file_location == suitelevel:
        file_location = caselevel
        suitename = casename
        listbox.delete('0', 'end')        
        for filename in get_filenames():
            listbox.insert(END, filename)
        
                
    #print ("selection:", selection, ": '%s'" % value)

def button_action(action):
    global start_time
    global end_time
    
    #fw.write(action+"\n")
    end_time = time.time()
    time_taken = abs(start_time - end_time)
    result_json = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
    #print(json.dumps(result_json, indent=4, separators=(',', ': ')))
    #subprocess.call("bash control.sh "+action)
    #ttime = int(time_taken)
    #if ttime > 0:
    if recordflag == 1:
        fw.write("sleep "+str(time_taken)+"\n")
        fw.write(action+"\n")    
    start_time = time.time()

class Application(Frame):
    def say_hi(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":7,"CODE":5,"ACTION":"KEYPRESS"}]})
        #button_action("INPUT")
        send_data(INPUT_data, "INPUT")		

    def playcase(self):
        global casename
        global suitename        

        if file_location == caselevel:        
            print(("playcase:", casename))
            #print("copy /rest/testcase/"+casename+" /rest/execute.txt")
            print((suitename+'/'+casename))    
            shutil.copy2(suitename +'/' + casename, '../execute.txt')
            self.say_playonce()
    
               
    def say_playonce(self):
                with open('../execute.txt') as f:
                    for line in f:
                        print (line)
                        if 'sleep' in line:
                            sleeptime=line[6:]
                            print(sleeptime)          
                            time.sleep(float(sleeptime))
                        else:
                            #subprocess.call("bash control.sh "+line)
                            if 'INPUT' in line:
                                self.say_hi()
                            elif 'MENU' in line:
                                self.say_menu()
                            elif 'EXIT' in line:
                                self.say_exit()
                            elif 'BACK' in line:
                                self.say_back()
                            elif 'INFO' in line:
                                self.say_info()
                            elif 'POWER' in line:
                                self.say_power()
                            elif 'OK' in line:
                                self.say_ok()
                            elif 'LEFT' in line:
                                self.say_left()
                            elif 'RIGHT' in line:
                                self.say_right()
                            elif 'UP' in line:
                                self.say_up()
                            elif 'DOWN' in line:
                                self.say_down()
                            elif 'CC' in line:
                                self.say_CC()
                            elif 'PIC_MODE' in line:
                                self.say_pic()
                            elif 'WIDE' in line:
                                self.say_wide()
                            elif 'VOLUP' in line:
                                self.say_volplus()
                            elif 'VOLDOWN' in line:
                                self.say_volmins()
                            elif 'CHUP' in line:
                                self.say_chplus()
                            elif 'CHDOWN' in line:
                                self.say_chmins()
                            elif 'VIA' in line:
                                self.say_vizio()
                            elif 'vudu' in line:
                                self.say_vudu()
                            elif 'netflix' in line:
                                self.say_netflix()
                            elif 'amazon' in line:
                                self.say_amazon()
                            elif 'xumo' in line:
                                self.say_xumo()
                            elif 'crackle' in line:
                                self.say_crackle()
                            elif 'iheart' in line:
                                self.say_iheart()
                            elif 'watchfree' in line:
                                self.say_watchfree()
                            elif '1' in line:
                                self.say_1()
                            elif '2' in line:
                                self.say_2()
                            elif '3' in line:
                                self.say_3()
                            elif '4' in line:
                                self.say_4()
                            elif '5' in line:
                                self.say_5()
                            elif '6' in line:
                                self.say_6()
                            elif '7' in line:
                                self.say_7()
                            elif '8' in line:
                                self.say_8()
                            elif '9' in line:
                                self.say_9()
                            elif '0' in line:
                                self.say_0()
                            elif 'takefilm' in line:
                                self.say_takefilm()                        
            

    
    def play_all(self):
        global casename
        global suitename        

        if file_location == caselevel:    
            for filename in get_filenames():
                casename = filename
                print(("playcase:", casename))
                #print("copy /rest/testcase/"+casename+" /rest/execute.txt")
                print((suitename+'/'+casename))    
                shutil.copy2(suitename +'/' + casename, '../execute.txt')
                self.say_playonce()
        

    def showsuites(self):
        global listbox
        global file_location        

        file_location = suitelevel        
        listbox.delete('0', 'end')        
        for suitename in get_suites():
            listbox.insert(END, suitename)
        
    def say_record(self):
        global recordflag
        global fw
        global start_time        
        
        if recordflag == 0:
            self.record["fg"]   = "red"
            self.record["text"] = "Stop"
            recordflag = 1
            fw= open("../execute.txt", "w")
            print("record start time")
            start_time = time.time()            
        else:
            recordflag = 0
            self.record["fg"]   = "black"
            self.record["text"] = "Record"
            fw.write("[end]")
            fw.close()

    def say_runcase(self):
        global casename
        
        print(("copy /rest/testcase/"+casename+" /rest/execute.txt"))
        os.system("copy /rest/testcase/"+casename+" /rest/execute.txt")
        
    def say_repeat(self):
        while True:
            with open('../execute.txt') as f:
                for line in f:
                    print (line)
                    if 'sleep' in line:
                        sleeptime=line[6:]
                        print(sleeptime)          
                        time.sleep(float(sleeptime))
                    else:
                        #subprocess.call("bash control.sh "+line)
                        if 'INPUT' in line:
                            self.say_hi()
                        elif 'MENU' in line:
                            self.say_menu()
                        elif 'EXIT' in line:
                            self.say_exit()
                        elif 'BACK' in line:
                            self.say_back()
                        elif 'INFO' in line:
                            self.say_info()
                        elif 'POWER' in line:
                            self.say_power()
                        elif 'OK' in line:
                            self.say_ok()
                        elif 'LEFT' in line:
                            self.say_left()
                        elif 'RIGHT' in line:
                            self.say_right()
                        elif 'UP' in line:
                            self.say_up()
                        elif 'DOWN' in line:
                            self.say_down()
                        elif 'CC' in line:
                            self.say_CC()
                        elif 'PIC_MODE' in line:
                            self.say_pic()
                        elif 'WIDE' in line:
                            self.say_wide()
                        elif 'VOLUP' in line:
                            self.say_volplus()
                        elif 'VOLDOWN' in line:
                            self.say_volmins()
                        elif 'CHUP' in line:
                            self.say_chplus()
                        elif 'CHDOWN' in line:
                            self.say_chmins()
                        elif 'VIA' in line:
                            self.say_vizio()
                        elif 'vudu' in line:
                            self.say_vudu()
                        elif 'netflix' in line:
                            self.say_netflix()
                        elif 'amazon' in line:
                            self.say_amazon()
                        elif 'xumo' in line:
                            self.say_xumo()
                        elif 'crackle' in line:
                            self.say_crackle()
                        elif 'iheart' in line:
                            self.say_iheart()
                        elif 'watchfree' in line:
                            self.say_watchfree()
                        elif '1' in line:
                            self.say_1()
                        elif '2' in line:
                            self.say_2()
                        elif '3' in line:
                            self.say_3()
                        elif '4' in line:
                            self.say_4()
                        elif '5' in line:
                            self.say_5()
                        elif '6' in line:
                            self.say_6()
                        elif '7' in line:
                            self.say_7()
                        elif '8' in line:
                            self.say_8()
                        elif '9' in line:
                            self.say_9()
                        elif 'takefilm' in line:
                            self.say_takefilm()                        
            
    def say_exit(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":3,"ACTION":"KEYPRESS"}]})
        #button_action("exit")
        send_data(EXIT_data, "EXIT")

    def say_power(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":11,"CODE":2,"ACTION":"KEYPRESS"}]})
        #button_action("power")
        send_data(POWER_data, "POWER")		
        
    def say_vudu(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "8", "MESSAGE": "https://my.vudu.com/castReceiver/index.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 0, "APP_ID": "36346174", "MESSAGE": "{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{\"launchedFromCustomIRButton\": true}}}"}})
        #button_action("vudu")
        send_data(VUDU_data,"vudu")

    def say_netflix(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 3, "APP_ID": "1", "MESSAGE": "http://127.0.0.1:12345/scfs/sctv/main.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 3, "APP_ID": "1", "MESSAGE": None}})
        #button_action("netflix")
        send_data(NETFLIX_data,"netflix")

    def say_amazon(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "4", "MESSAGE": "https://atv-ext.amazon.com/blast-app-hosting/html5/index.html?deviceTypeID=A3OI4IHTNZQWDD"}})
        #button_action("amazon")
        send_data(AMAZON_data,"amazon")

    def say_xumo(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "6", "MESSAGE": "https://vizio-smartcast-app.xumo.com/latest/index.html"}})
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 0, "APP_ID": "36E1EA1F", "MESSAGE": "{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{}}}"}})
        #button_action("xumo")
        send_data(XUMO_data,"xumo")

    def say_crackle(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "5", "MESSAGE": "https://crackleott.s3.amazonaws.com/vizio/prod/index.html?cmpid=Vizio_Remote_Launch"}})
        #button_action("crackle")
        send_data (CRACKLE_data,"crackle")
        

    def say_iheart(self):
        global uri
        global payload
    
        #uri = "https://" + IP + ":" + PORT + "/app/launch"
        #payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": 2, "APP_ID": "6", "MESSAGE": "https://tv.iheart.com/smartcast/"}})
        #button_action("iheart")
        send_data (IHEART_data,"iheart")
    
    def say_watchfree(self):
        send_data (WatchFree_data,"watchfree")
        
    def say_menu(self):
        #global uri
        #global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":8,"ACTION":"KEYPRESS"}]})
        #button_action("MENU")
        print("...menu")		
        send_data(MENU_data, "MENU")
        
    def say_mute(self):
        
        print("...mute")		
        send_data(MUTE_data, "MUTE")    
        
    def say_up(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":8,"ACTION":"KEYPRESS"}]})
        #button_action("up")
        send_data(UP_data, "UP")		
        
    def say_left(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("left")
        send_data(LEFT_data, "LEFT")		
        
    def say_right(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":7,"ACTION":"KEYPRESS"}]})
        #button_action("right")
        send_data(RIGHT_data, "RIGHT")		
        
    def say_down(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("down")
        send_data(DOWN_data, "DOWN")		
        
    def say_ok(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":3,"CODE":2,"ACTION":"KEYPRESS"}]})
        #button_action("ok")
        send_data(OK_data, "OK")		
        
    def say_back(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("back")
        send_data(BACK_data, "BACK")		
        
    def say_info(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":6,"ACTION":"KEYPRESS"}]})
        #button_action("info")
        send_data(INFO_data,"INFO")
        
    def say_CC(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":13,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("CC")
        send_data(CC_data,"CC")
        
    def say_pic(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":6,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("pic")
        send_data(PIC_data,"PIC_MODE")
        
    def say_wide(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":6,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("pic")
        send_data(WIDE_data,"WIDE")    
        
    def say_vizio(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":4,"CODE":15,"ACTION":"KEYPRESS"}]})
        #button_action("vizio")
        send_data(VIA_data,"VIA")
        
    def say_volplus(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":5,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("volplus")
        send_data(VOLUP_data, "VOLUP")		
        
    def say_volmins(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":5,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("volmins")
        send_data(VOLDOWN_data, "VOLDOWN")		
        
    def say_chplus(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":8,"CODE":1,"ACTION":"KEYPRESS"}]})
        #button_action("chplus")
        send_data(CHUP_data, "CHUP")		
        
    def say_chmins(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":8,"CODE":0,"ACTION":"KEYPRESS"}]})
        #button_action("chmins")
        send_data(CHDOWN_data, "CHDOWN")		
        
    def say_1(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":49,"ACTION":"KEYPRESS"}]})
        #button_action("1")
        send_data(ONE_data, "1")		
        
    def say_2(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":50,"ACTION":"KEYPRESS"}]})
        #button_action("2")
        send_data(TWO_data, "2")
        
    def say_3(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":51,"ACTION":"KEYPRESS"}]})
        #button_action("3")
        send_data(THREE_data, "3")		
        
    def say_4(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":52,"ACTION":"KEYPRESS"}]})
        #button_action("4")
        send_data(FOUR_data, "4")		
        
    def say_5(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":53,"ACTION":"KEYPRESS"}]})
        #button_action("5")
        send_data(FIVE_data, "5")		
        
    def say_6(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":54,"ACTION":"KEYPRESS"}]})
        #button_action("6")
        send_data(SIX_data, "6")		
        
    def say_7(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":55,"ACTION":"KEYPRESS"}]})
        #button_action("7")
        send_data(SEVEN_data, "7")		
        
    def say_8(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"Csend_data(MENU_data)ODESET":0,"CODE":56,"ACTION":"KEYPRESS"}]})
        #button_action("8")
        send_data(EIGHT_data, "8")		
        
    def say_9(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":57,"ACTION":"KEYPRESS"}]})
        #button_action("9")
        send_data(NINE_data, "9")	
    
    def say_0(self):
        global uri
        global payload
        
        #uri = "https://" + IP + ":" + PORT + "/key_command/"
        #payload = json.dumps({"KEYLIST": [{"CODESET":0,"CODE":57,"ACTION":"KEYPRESS"}]})
        #button_action("9")
        send_data(ZERO_data, "0")    

    #def say_save(self):
    #    button_action("save")
        
    def say_takefilm(self):
        #button_action("takefilm")
        #os.system('c:\\sikuli\\runsikulix.cmd -r c:\\sikuli\\takefilm.sikuli')
        #process = subprocess.Popen('python', 'takefilm.py', 'case1')
        process = subprocess.Popen(["python", "takefilm.py", "case1"], stdout=subprocess.PIPE)
        button_action("takefilm")        
        
    def say_pair(self):
        global ip_text
        global AUTH_TOKEN
        global IP
        global HEADERS
        #subprocess.call("bash control.sh pair "+ip_text.get())        
        #button_action("pair")
        
        pincode=""
        print((ip_text.get()))
        IP = ip_text.get()
        IP = E1.get()

        fh= open("iphistory.txt","w")
        fh.write(IP)
        fh.close()

        if UseRest:		
            ####################################################################################
            HEADERS = {"Content-Type": "application/json"}        
            fau = open("authtoken.log","r")
            AUTH_TOKEN = fau.read()
            fau.close()
            HEADERS = {"auth": AUTH_TOKEN, "Content-Type": "application/json"}
            uri = "https://" + IP + ":" + PORT + "/key_command/"
            payload = json.dumps({"KEYLIST": [{"CODESET":7,"CODE":5,"ACTION":"KEYPRESS"}]})
            result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
            print(result)
            if(result["STATUS"]["RESULT"] != "SUCCESS"):
                AUTH_TOKEN = get_authtoken()        
                HEADERS = {"auth": AUTH_TOKEN, "Content-Type": "application/json"}

    def say_save(self):
        print((file_text.get()))
        #os.system('copy execute.txt '+file_text.get())
        #shutil.copy2('rest/execute.txt', '/rest/testcase/'+file_text.get())
        currdir = os.getcwd()
        #tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        #print(tempdir+'/'+file_text.get())
        shutil.copy2('../execute.txt', tempdir + '/' + file_text.get())
        #updatebox(file_text.get())        

    def say_insert(self):
        global timeout_text
        global recordflag        

        if recordflag == 1:
            print((timeout_text.get()))
            fw.write("sleep "+str(timeout_text.get())+"\n")            
        
    def say_quit(self):
        print("start calling exit...")    
        #sys.exit(0)
        #print("Done exit")        
        #try:
        #    sys.exit()
        #except:
        #    print(sys.exc_info()[0])
        os._exit(1)        
        
    def createWidgets(self):
        global listbox    
    
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["font"] = "Helvetica 10 bold"
        self.QUIT["command"] =  self.say_quit
        self.QUIT.grid(column=3, row=18)
        self.QUIT.config(width=8, height=2)

        button_pair = Button(self)
        button_pair["text"] = "Pair"
        button_pair["command"] =  self.say_pair
        button_pair.grid(column=0, row=19)
        button_pair.config(width=6, height=1)
        
        button_save = Button(self)
        button_save["text"] = "Save File"
        button_save["command"] =  self.say_save
        button_save.grid(column=3, row=19)
        button_save.config(width=6, height=1)

        button_insert = Button(self)
        button_insert["text"] = "Insert"
        button_insert["command"] =  self.say_insert
        button_insert.grid(column=6, row=19)
        button_insert.config(width=6, height=1)
        
        #button_pair = Button(self)
        #button_pair["text"] = "Run Case"
        #button_pair["command"] =  self.say_runcase
        #button_pair.grid(column=6, row=18)
        
        self.record = Button(self)
        self.record["text"] = "Record",
        self.record["command"] = self.say_record
        self.record.grid(column=3, row=17)
        self.record.config(width=6, height=1)

        self.repeat = Button(self)
        self.repeat["text"] = "Repeat",
        self.repeat["command"] = self.say_repeat
        self.repeat.grid(column=6, row=18)
        self.repeat.config(width=6, height=1)
        
        button_input = Button(self)
        button_input["text"] = "INPUT",
        button_input["command"] = self.say_hi
        button_input.grid(column=0, row=1)
        button_input.config(width=6, height=1)

        button_power = Button(self)
        button_power["text"] = "power",
        button_power["command"] = self.say_power
        button_power.grid(column=6, row=1)
        button_power.config(width=6, height=1)

        button_vudu = Button(self)
        button_vudu["text"] = "VUDU",
        button_vudu["command"] = self.say_vudu
        button_vudu.grid(column=0, row=2)
        button_vudu["fg"]   = "blue"        
        button_vudu.config(width=8, height=1)

        button_netflix = Button(self)
        button_netflix["text"] = "NETFLIX",
        button_netflix["command"] = self.say_netflix
        button_netflix.grid(column=3, row=2)
        button_netflix["fg"]   = "red"
        button_netflix.config(width=8, height=1)
        
        button_amazon = Button(self)
        button_amazon["text"] = "AMAZON",
        button_amazon["command"] = self.say_amazon
        button_amazon.grid(column=5, row=2)
        button_amazon["fg"]   = "magenta"    
        button_amazon.config(width=8, height=1)
        
        button_xumo = Button(self)
        button_xumo["text"] = "XUMO",
        button_xumo["command"] = self.say_xumo
        button_xumo.grid(column=0, row=3)
        button_xumo["fg"]   = "green"    
        button_xumo.config(width=8, height=1)
        
        button_crackle = Button(self)
        button_crackle["text"] = "CRACKLE",
        button_crackle["command"] = self.say_crackle
        button_crackle.grid(column=3, row=3)
        button_crackle["fg"]   = "brown"
        button_crackle.config(width=8, height=1)        

        button_iheart = Button(self)
        button_iheart["text"] = "iHeart",
        button_iheart["command"] = self.say_iheart
        button_iheart.grid(column=5, row=3)
        button_iheart["fg"]   = "orange"    
        button_iheart.config(width=8, height=1)
        
        button_watchfree = Button(self)
        button_watchfree["text"] = "WatchFree",
        button_watchfree["command"] = self.say_watchfree
        button_watchfree.grid(column=6, row=3)
        button_watchfree["fg"]   = "lightblue"    
        button_watchfree.config(width=8, height=1)        
        
        button_exit = Button(self)
        button_exit["text"] = "exit",
        button_exit["command"] = self.say_exit
        button_exit.grid(column=0, row=4)
        button_exit.config(width=6, height=1)

        button_menu = Button(self)
        button_menu["text"] = "MENU",
        button_menu["command"] = self.say_menu
        button_menu.grid(column=6, row=4)
        button_menu.config(width=6, height=1)
        
        button_mute = Button(self)
        button_mute["text"] = "Mute",
        button_mute["command"] = self.say_mute
        button_mute.grid(column=0, row=5)
        button_mute.config(width=4, height=1)        
        
        button_up = Button(self)
        button_up["text"] = "up",
        button_up["command"] = self.say_up
        button_up.grid(column=3, row=5)
        button_up.config(width=4, height=1)

        button_left = Button(self)
        button_left["text"] = "left",
        button_left["command"] = self.say_left
        button_left.grid(column=2, row=6)
        button_left.config(width=4, height=1)

        button_right = Button(self)
        button_right["text"] = "right",
        button_right["command"] = self.say_right
        button_right.grid(column=4, row=6)
        button_right.config(width=4, height=1)

        button_down = Button(self)
        button_down["text"] = "down",
        button_down["command"] = self.say_down
        button_down.grid(column=3, row=7)
        button_down.config(width=4, height=1)

        button_ok = Button(self)
        button_ok["text"] = "OK",
        button_ok["command"] = self.say_ok
        button_ok.grid(column=3, row=6)
        button_ok.config(width=5, height=2)

        button_back = Button(self)
        button_back["text"] = "back",
        button_back["command"] = self.say_back
        button_back.grid(column=0, row=8)

        button_cc = Button(self)
        button_cc["text"] = "CC",
        button_cc["command"] = self.say_CC
        button_cc.grid(column=3, row=8)

        button_info = Button(self)
        button_info["text"] = "info",
        button_info["command"] = self.say_info
        button_info.grid(column=6, row=8)

        button_volplus = Button(self)
        button_volplus["text"] = "VOL+",
        button_volplus["command"] = self.say_volplus
        button_volplus.grid(column=0, row=9)

        button_volmis = Button(self)
        button_volmis["text"] = "VOL-",
        button_volmis["command"] = self.say_volmins
        button_volmis.grid(column=0, row=10)

        button_vizio = Button(self,height=2, width=6)
        button_vizio["text"] = "VIZIO",
        button_vizio["command"] = self.say_vizio
        button_vizio.grid(column=3, row=9)
        
        button_0 = Button(self)
        button_0["text"] = "0",
        button_0["command"] = self.say_0
        button_0.grid(column=3, row=10)

        button_chplus = Button(self)
        button_chplus["text"] = "CH+",
        button_chplus["command"] = self.say_chplus
        button_chplus.grid(column=6, row=9)
        
        button_chmis = Button(self)
        button_chmis["text"] = "CH-",
        button_chmis["command"] = self.say_chmins
        button_chmis.grid(column=6, row=10)
        
        button_1 = Button(self)
        button_1["text"] = "1",
        button_1["command"] = self.say_1
        button_1.grid(column=0, row=11)

        button_2 = Button(self)
        button_2["text"] = "2",
        button_2["command"] = self.say_2
        button_2.grid(column=3, row=11)

        button_3 = Button(self)
        button_3["text"] = "3",
        button_3["command"] = self.say_3
        button_3.grid(column=6, row=11)

        button_4 = Button(self)
        button_4["text"] = "4",
        button_4["command"] = self.say_4
        button_4.grid(column=0, row=12)

        button_5 = Button(self)
        button_5["text"] = "5",
        button_5["command"] = self.say_5
        button_5.grid(column=3, row=12)

        button_6 = Button(self)
        button_6["text"] = "6",
        button_6["command"] = self.say_6
        button_6.grid(column=6, row=12)

        button_7 = Button(self)
        button_7["text"] = "7",
        button_7["command"] = self.say_7
        button_7.grid(column=0, row=13)

        button_8 = Button(self)
        button_8["text"] = "8",
        button_8["command"] = self.say_8
        button_8.grid(column=3, row=13)

        button_9 = Button(self)
        button_9["text"] = "9",
        button_9["command"] = self.say_9
        button_9.grid(column=6, row=13)
        
        button_pic = Button(self)
        button_pic["text"] = "PIC",
        button_pic["command"] = self.say_pic
        button_pic.grid(column=0, row=17)  
        button_pic.config(width=6, height=1)
        
        button_wide = Button(self)
        button_wide["text"] = "WIDE",
        button_wide["command"] = self.say_wide
        button_wide.grid(column=6, row=17)  
        button_wide.config(width=6, height=1)        

        button_takefilm = Button(self)
        button_takefilm["text"] = "Film",
        button_takefilm["command"] = self.say_takefilm
        button_takefilm.grid(column=0, row=18)
        button_takefilm.config(width=6, height=1)

##################################################
        w = Label(root, text=" TEST CASES ", font=("Helvetica 10 bold"))
        w.pack(padx=6, pady=4)

        scrollbar = Scrollbar(root, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        listbox = Listbox(root,width=30, height=5, yscrollcommand=scrollbar.set)
        listbox.pack()

        for suitename in get_suites():
            listbox.insert(END, suitename)
        # attach listbox to scrollbar
        #listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        listbox.bind("<Double-Button-1>", OnDouble)
##################################################
        frame4 = Frame(root)
        frame4.pack()
        playbutton = Button(frame4, text="Suites",width=8, height=1, fg="green", command=self.showsuites)
        playbutton.pack( side=LEFT, padx=2, pady=2 )
        playbutton = Button(frame4, text="Play case",width=8, height=1, fg="blue", command=self.playcase)
        playbutton.pack( side=LEFT, padx=2, pady=2 )
        playallbutton = Button(frame4, text="Play all",width=8, height=1, fg="brown", command=self.play_all)
        playallbutton.pack( side=LEFT, padx=2, pady=2 )
#####################################################        
        
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
if __name__ == '__main__':
    
    global start_time    
    root = Tk()
    root.title("V-Silicon QA Automation Testing Tool")
    root.geometry("360x760+10+10") 
    #image = PhotoImage(file="v-silicon.png")
    #image = image.subsample(2, 2)
    #label = Label(image=image)
    #label.pack()
    
    image = Image.open('../icons/v-silicon.png')
    display = ImageTk.PhotoImage(image)
    label = Label(root, image=display)
    label.pack()
    
    app = Application(master=root)
    
    #fh = open("iphistory.txt", "r") 
    #IP = fh.read()
    #fh.close()
    print(IP)
    ##############################################################################
    #subprocess.call(["adb", "disconnect"])
    #subprocess.call(["adb", "connect", IP])
    #process = subprocess.Popen(["adb", "shell", "logcat"], stdout=subprocess.PIPE)
    #stdout_queue = queue.Queue()
    #stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    #stdout_reader.start()
    ##############################################################################
    frame1 = Frame(root)
    frame1.pack(fill=X)
    L1 = Label(frame1, text="IP : ", width=8)
    L1.pack(side = LEFT, padx=5, pady=5)
    ip_text = StringVar()
    E1 = Entry(frame1, textvariable=ip_text)
    E1.insert(END, IP)
    E1.place(relx=0.5, rely=0.5, anchor='n')
    #E1.pack(padx=5, expand=True)        
    
    frame3 = Frame(root)
    frame3.pack(fill=X)
    L3 = Label(frame3, text="File name : ", width=8)
    L3.pack(side = LEFT, padx=5, pady=5)
    file_text = StringVar()
    E3 = Entry(frame3, textvariable=file_text)
    E3.place(relx=0.5, rely=0.5, anchor='n')
    #E3.pack(padx=5, expand=True)
    #savebutton = Button(frame3, text="Save File", fg="brown", command=Savefile)
    #savebutton.pack( side = LEFT )
    
    frame5 = Frame(root)
    frame5.pack(fill=X)
    L5 = Label(frame5, text="Timeout : ", width=8)
    L5.pack(side = LEFT, padx=5, pady=5)
    timeout_text = StringVar()
    E5 = Entry(frame5, textvariable=timeout_text)
    E5.place(relx=0.5, rely=0.5, anchor='n')
    #E5.pack(padx=5, expand=True)        
    #####################################################################################        
    recordflag = 0
    start_time = time.time()
    root.mainloop()
    #fw.write("[end]")
    #fw.close()
    #fh.close()
    #root.destroy()
    root.quit()





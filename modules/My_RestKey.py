import json
import requests
import simplejson
import time
import shutil
import os
from modules.TestCfgParse import TestCfgParse,CfgParse
Auth_Token = "./Config/Auth_Token.txt"
requests.packages.urllib3.disable_warnings()
nommalKeyDict={
                "KEYBOARD_BACKSPACE":(0, 8),
                "KEYBOARD_TAB":(0, 9),
                "KEYBOARD_SPACE":(0, 32),
                "KEYBOARD_EXClAMATION":(0, 33),
                "KEYBOARD_DOUBLE_QUOTES":(0, 34),
                "KEYBOARD_NUMBER":(0, 35),
                "KEYBOARD_DOLLAR":(0, 36),
                "KEYBOARD_PERCENT":(0, 37),
                "KEYBOARD_AND":(0, 38),
                "KEYBOARD_SIGNLE_QUOTES":(0, 39),
                "KEYBOARD_LEFT_PARENTHESES":(0, 40),
                "KEYBOARD_RIGHT_PARENTHESES":(0, 41),
                "KEYBOARD_ASTERISK":(0, 42),
                "KEYBOARD_PLUS":(0, 43),
                "KEYBOARD_COMMA":(0, 44),
                "DOT":(0, 45),
                "KEYBOARD_FULL_STOP":(0, 46),
                "KEYBOARD_BACKSLASH":(0, 47),
                "0":(0, 48),
                "1":(0, 49),
                "2":(0, 50),
                "3":(0, 51),
                "4":(0, 52),
                "5":(0, 53),
                "6":(0, 54),
                "7":(0, 55),
                "8":(0, 56),
                "9":(0, 57),
                "KEYBOARD_COLON":(0, 58),
                "KEYBOARD_SEMICOLON":(0, 59),
                "KEYBOARD_LEFT_CHEVRONS":(0, 60),
                "KEYBOARD_EQUALS":(0, 61),
                "KEYBOARD_RIGHT_CHEVRONS":(0, 62),
                "KEYBOARD_QUESTION":(0, 63),
                "KEYBOARD_AT":(0, 64),
                "KEYBOARD_A":(0, 65),
                "KEYBOARD_B":(0, 66),
                "KEYBOARD_C":(0, 67),
                "KEYBOARD_D":(0, 68),
                "KEYBOARD_E":(0, 69),
                "KEYBOARD_F":(0, 70),
                "KEYBOARD_G":(0, 71),
                "KEYBOARD_H":(0, 72),
                "KEYBOARD_I":(0, 73),
                "KEYBOARD_J":(0, 74),
                "KEYBOARD_K":(0, 75),
                "KEYBOARD_L":(0, 76),
                "KEYBOARD_M":(0, 77),
                "KEYBOARD_N":(0, 78),
                "KEYBOARD_O":(0, 79),
                "KEYBOARD_P":(0, 80),
                "KEYBOARD_Q":(0, 81),
                "KEYBOARD_R":(0, 82),
                "KEYBOARD_S":(0, 83),
                "KEYBOARD_T":(0, 84),
                "KEYBOARD_U":(0, 85),
                "KEYBOARD_V":(0, 86),
                "KEYBOARD_W":(0, 87),
                "KEYBOARD_X":(0, 88),
                "KEYBOARD_Y":(0, 89),
                "KEYBOARD_Z":(0, 90),
                "KEYBOARD_LEFT_BRACKETS":(0, 91),
                "KEYBOARD_SLASH":(0, 92),
                "KEYBOARD_RIGHT_BRACKETS":(0, 93),
                "KEYBOARD_CARET":(0, 94),
                "KEYBOARD_UNDERSCORE":(0, 95),
                "KEYBOARD_ACCENT":(0, 96),
                "KEYBOARD_a":(0, 97),
                "KEYBOARD_b":(0, 98),
                "KEYBOARD_c":(0, 99),
                "KEYBOARD_d":(0, 100),
                "KEYBOARD_e":(0, 101),
                "KEYBOARD_f":(0, 102),
                "KEYBOARD_g":(0, 103),
                "KEYBOARD_h":(0, 104),
                "KEYBOARD_i":(0, 105),
                "KEYBOARD_j":(0, 106),
                "KEYBOARD_k":(0, 107),
                "KEYBOARD_l":(0, 108),
                "KEYBOARD_m":(0, 109),
                "KEYBOARD_n":(0, 110),
                "KEYBOARD_o":(0, 111),
                "KEYBOARD_p":(0, 112),
                "KEYBOARD_q":(0, 113),
                "KEYBOARD_r":(0, 114),
                "KEYBOARD_s":(0, 115),
                "KEYBOARD_t":(0, 116),
                "KEYBOARD_u":(0, 117),
                "KEYBOARD_v":(0, 118),
                "KEYBOARD_w":(0, 119),
                "KEYBOARD_x":(0, 120),
                "KEYBOARD_y":(0, 121),
                "KEYBOARD_z":(0, 122),
                "KEYBOARD_LEFT_BRACE":(0, 123),
                "KEYBOARD_BRA":(0, 124),
                "KEYBOARD_RIGHT_BRACE":(0, 125),
                "KEYBOARD_TITLE":(0, 126),
                "KEYBOARD_DEL":(0, 127),
                "KEYBOARD_ALT":(1, 0),
                "KEYBOARD_CAPS":(1, 1),
                "KEYBOARD_SHIFT":(1, 2),
                "KEYBOARD_COM":(1, 3),
                "FORWARD":(2,0), 
                "REWIND":(2, 1),
                "PAUSE":(2, 2),
                "PLAY":(2, 3),
                "RECORD":(2, 4),
                "STOP":(2, 9),
                "TRACK_FORWARD":(2, 10),
                "TRACK_REVERSE":(2, 11),
                "DOWN":(3,0), 
                "LEFT":(3, 1),
                "OK":(3, 2),
                "RIGHT":(3, 7),
                "UP":(3, 8),
                "KEYBOARD_UP":(3, 6),
                "KEYBOARD_DOWN":(3, 3),
                "KEYBOARD_LEFT":(3, 4),
                "KEYBOARD_RIGHT":(3, 5),
                "KEYBOARD_ENTER":(3, 2),
                "BACK":(4,0), 
                "CANCEL":(4, 1),
                "EXIT":(4, 3),
                "EPG":(4, 4),
                "BANNER":(4, 6),
                "MENU":(4, 8),
                "VIA":(4, 15),
                "LINK":(4, 16),
                "STORE_DEMO":(4, 17),
                "VOLDOWN":(5,0), 
                "VOLUP":(5, 1),
                "MUTE":(5, 4),
                "PIC_MODE":(6,0), 
                "POP":(6, 2),
                "INPUT":(7, 5),
                "CHDOWN":(8,0), 
                "CHUP":(8, 1),
                "LAST":(8, 2),
                "KEYBOARD_RED":(9,0), 
                "KEYBOARD_GREEN":(9, 1),
                "KEYBOARD_BLUE":(9, 2),
                "KEYBOARD_YELLOW":(9, 3),
                "POWER_OFF":(11,0), 
                "POWER_ON":(11, 1),
                "POWER_TOGGLE":(11, 2),
                "3D_MODE_CYCLE":(12, 7),
                "CC":(13, 1),
                "FACTORY_TEST_01":(14,1), 
                "FACTORY_TEST_02":(14,2), 
                "FACTORY_TEST_03":(14,3), 
                "FACTORY_TEST_04":(14,4), 
                "FACTORY_TEST_05":(14,5), 
                "FACTORY_TEST_06":(14,6), 
                "FACTORY_TEST_07":(14,7), 
                "FACTORY_TEST_08":(14,8), 
                "FACTORY_TEST_09":(14,9), 
                "FACTORY_TEST_10":(14,10), 
                "FACTORY_TEST_11":(14,11), 
                "FACTORY_TEST_12":(14,12), 
                "FACTORY_TEST_13":(14,13), 
                "FACTORY_TEST_14":(14,14), 
                "FACTORY_TEST_15":(14,15), 
                "FACTORY_TEST_16":(14,16), 
    
              }
OTTKeyDict = {
            "cast-vudu":(0,"36346174","{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{\"launchedFromCustomIRButton\": true}}}"),
            "cast-xumo":(0,"36E1EA1F","{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{}}}"),
            "SmartCastTV":(2,"1","http://127.0.0.1:12345/scfs/sctv/main.html"),
            "cast-haystacktv":(0,"898AF734","{\"CAST_NAMESPACE\":\"urn:x-cast:com.google.cast.media\",\"CAST_MESSAGE\":{\"type\":\"LOAD\",\"media\":{},\"autoplay\":true,\"currentTime\":0,\"customData\":{\"platform\":\"sctv\"}}}"),
            "cast-html5-hulu":(2,"3","https://viziosmartcast.app.hulu.com/livingroom/viziosmartcast/1/index.html#initialize"),
            "cast-html5-amazon":(2,"4","https://atv-ext.amazon.com/blast-app-hosting/html5/index.html?deviceTypeID=A3OI4IHTNZQWDD"),
            "cast-html5-crackle":(2,"5","https://crackleott.s3.amazonaws.com/vizio/prod/index.html?cmpid=Vizio_Remote_Launch"),
            "cast-html5-iheart":(2,"6","https://tv.iheart.com/smartcast/"),
            "cast-html5-fandangoNow":(2,"7","https://www-viziosmartcast.mgo.com/"),
            "cast-html5-plex":(2,"9","https://plex.tv/web/tv/vizio-smartcast"),
            "cast-html5-NBC":(2,"10","https://vizioapp.nbc.co/"),
            "cast-html5-baeble":(2,"11","https://smartcast.baeblemusic.com/"),
            "cast-html5-curiositystream":(2,"12","https://tv-vizio.curiositystream.com/"),
            "cast-html5-cookingpanda":(2,"13","https://html5.cookingpanda.com/"),
            "cast-html5-opposingviews":(2,"14","https://html5.opposingviews.com/"),
            "cast-html5-newsy":(2,"15","https://apps.newsy.com/vizio/"),
            "cast-html5-dovechannel":(2,"16","https://www.dovechannel.com/viziosmartcast/"),
            "cast-html5-mammoth":(2,"17","http://cast.thatmatt.me/sctv/index.html"),
            "cast-html5-contv":(2,"18","https://www.contv.com/viziosmartcast/"),
            "cast-html5-toongoggles":(2,"21","https://html5.toongoggles.com/?ua=viziosmartcast"),
            "cast-html5-pluto":(2,"22","https://vizio.pluto.tv"),
            "cast-html5-filmrise":(2,"24","https://iptv.fawesome.tv/?iptv=true&siteId=898&platform_id=1217562"),
            "cast-html5-justlol":(2,"25","https://www.justlol.tv/tv/vizio"),
            "cast-html5-tasteit":(2,"26","https://www.tasteit.tv/tv/vizio"),
            "cast-html5-asiancrush":(2,"27","https://html5.asiancrush.com/?ua=viziosmartcast"),
            "cast-html5-midnightpulp":(2,"28","https://html5.midnightpulp.com/?ua=viziosmartcast"),
            "cast-html5-yuyutv":(2,"29","https://html5.yuyutv.com/?ua=viziosmartcast"),
            "cast-html5-kmtv":(2,"30","https://html5.kmtvnow.com/?ua=viziosmartcast"),
            "cast-html5-vudu":(2,"31","https://my.vudu.com/castReceiver/index.html?launch-source=app-icon"),
            "cast-html5-dazn":(2,"34","https://tv.dazn.com/app/smartcast/index.html"),
            "cast-html5-flixfling":(2,"36","https://tv.flixfling.com/vizio-smartcast"),
            "cast-html5-cbs":(2,"37","https://www.cbs.com/smart-tv-apps/vizio/"),
            "cast-html5-fitfusion":(2,"39","https://apps.appmastery.co/apps/fitfusion/vizio/index.html"),
            "cast-html5-redbox":(2,"41","https://digital.redbox.com/cedevices/Vizio/prod/index.html"),
            "cast-html5-cbsn":(2,"37","https://www.cbs.com/smart-tv-apps/vizio/"),
            "cast-html5-cbsnews":(2,"42","https://ott.cbsnews.com/vizio/"),
            #Chromium Apps                     
            "chromium-html5-sctv":(4,"1", "http://127.0.0.1:12345/scfs/sctv/main.html"),
            "chromium-html5-hulu":(4,"3","https://viziosmartcast.app.hulu.com/livingroom/viziosmartcast/1/index.html#initialize"),
            "chromium-html5-amazon":(4,"4", "https://atv-ext.amazon.com/blast-app-hosting/html5/index.html?deviceTypeID=A3OI4IHTNZQWDD"),
            "chromium-html5-crackle":(4,"5","https://crackleott.s3.amazonaws.com/vizio/prod/index.html"),
            "chromium-html5-iheart":(4,"6", "https://tvclient.iheart.com/vizio"),
            "chromium-html5-mgo1":(4,"7", "https://www-viziosmartcast.mgo.com/"),
            "chromium-html5-tvinteractive":(4,"8","https://optin-staging.tvinteractive.tv/tos?commtype=JSONP&settings=514&h=64ca47b4ad575848e86da5f2d4d13715&ignore=513&token=23428506_97361_405036622&version=512&eid=ENG01&timeout=300000&gid=TOS02&local=http%3A%2F%2Ftvapi.tvinteractive.tv%3A8080&agree=515"),
            "chromium-html5-plex":(4,"9", "https://plex.tv/web/tv/vizio-smartcast"),
            "chromium-html5-nbc":(4,"10", "https://vizioapp.nbc.co/"),
            "chromium-html5-baeblemusic":(4,"11", "https://smartcast.baeblemusic.com/"),
            "chromium-html5-curiositystream":(4,"12", "https://tv-vizio.curiositystream.com/"),
            "chromium-html5-cookingpanda":(4,"13", "https://html5.cookingpanda.com/"),
            "chromium-html5-opposingviews":(4,"14", "https://html5.opposingviews.com/"),
            "chromium-html5-newsy":(4,"15", "https://apps.newsy.com/vizio/"),
            "chromium-html5-dovechannel":(4,"16", "https://www.dovechannel.com/viziosmartcast/"),
            "chromium-html5-thatmatt":(4,"17", "http://cast.thatmatt.me/sctv/index.html"),
            "chromium-html5-contv":(4,"18", "https://www.contv.com/viziosmartcast/"),
            "chromium-html5-mgo2":(4,"19", "https://stg-viziosmartcast.mgo.com"),
            "chromium-html5-plutotv1":(4,"20", "http://vizio.distribution.staging.pluto.tv.s3-website-us-east-1.amazonaws.com/"),
            "chromium-html5-toongoggles":(4,"21", "https://html5.toongoggles.com/?ua=viziosmartcast"),
            "chromium-html5-plutotv2":(4,"22", "https://vizio.pluto.tv"),
            "chromium-html5-scfsindex":(4,"23","http://127.0.0.1:12345/scfs/schk/index.html"),
            "chromium-html5-fawesome":(4,"24", "https://iptv.fawesome.tv/?iptv=true&siteId=898&platform_id=1217562"),
            "chromium-html5-justlol":(4,"25", "https://www.justlol.tv/tv/vizio"),
            "chromium-html5-tasteit":(4,"26", "https://www.tasteit.tv/tv/vizio"),
            "chromium-html5-asiancrush":(4,"27", "https://html5.asiancrush.com/?ua=viziosmartcast"),
            "chromium-html5-midnightpulp":(4,"28","https://html5.midnightpulp.com/?ua=viziosmartcast"),
            "chromium-html5-yuyutv":(4,"29","https://html5.yuyutv.com/?ua=viziosmartcast"),
            "chromium-html5-kmtvnow":(4,"30","https://html5.kmtvnow.com/?ua=viziosmartcast"),
            "chromium-html5-vudu":(4,"31", "https://my.vudu.com/castReceiver/index.html?launch-source=app-icon"),
            "chromium-html5-cloudfront":(4,"32", "https://d2wa4upmkzpg8j.cloudfront.net/index.html#/"),
            "chromium-html5-amazonaws":(4,"33", "https://s3-us-west-2.amazonaws.com/vizio-uat-web-client/index.html"),
            "chromium-html5-dazn":(4,"34","https://tv.dazn.com/app/smartcast/index.html"),
            "chromium-html5-scfsmain":(4,"35","http://127.0.0.1:12345/scfs/sctv/main.html"),
            "chromium-html5-flixfling":(4,"36", "https://tv.flixfling.com/vizio-smartcast"),
            "chromium-html5-cbs":(4,"37", "https://www.cbs.com/smart-tv-apps/vizio/"),
            "chromium-html5-moviesanywhere":(4,"38", "https://vizio-client.moviesanywhere.com/"),
            "chromium-html5-fitfusion":(4,"39", "https://apps.appmastery.co/apps/fitfusion/vizio/index.html"),
            "chromium-html5-learn2program":(4,"40","https://apps.appmastery.co/apps/learn2program/vizio/index.html"),
            "chromium-html5-redbox":(4,"41", "https://vizio.prod.redbox.com"),
            "chromium-html5-cbsnews":(4,"42", "https://ott.cbsnews.com/vizio/"),
            "chromium-html5-broadwayhd":(4,"43", "https://videos.broadwayhd.com/tv/vizio"),
            "chromium-html5-adventuresportsnetwork":(4,"44", "https://videos.adventuresportsnetwork.com/tv/vizio"),
            "chromium-html5-battlezone":(4,"45", "https://www.battlezone.tv/tv/vizio"),
            "chromium-html5-levelone":(4,"46", "https://levelone.unreel.me/tv/vizio "),
            "chromium-html5-globalreport":(4,"47", "https://globalreport.unreel.me/tv/vizio"),
            "chromium-html5-vidsgoneviral":(4,"48", "https://vidsgoneviral.unreel.me/tv/vizio"),
            "chromium-html5-throttle":(4,"49", "https://www.throttle.tv/tv/vizio"),
            "chromium-html5-pumbakidstv":(4,"50", "https://pumbakidstv.unreel.me/tv/vizio"),
            "chromium-html5-funzone":(4,"51", "https://funzone.unreel.me/tv/vizio"),
            "chromium-html5-whamnetwork":(4,"52", "https://whamnetwork.unreel.me/tv/vizio"),
            "chromium-html5-bumblebee":(4,"53", "https://www.bumblebee.tv/tv/vizio"),
            "chromium-html5-nowyouknow":(4,"54", "https://nowyouknow.unreel.me/tv/vizio"),
            "chromium-html5-cocoro":(4,"55", "https://html5.cocoro.tv/?ua=viziosmartcast"),
            "chromium-html5-tvgam":(4,"56","http://apps.tvgam.es/tv_games/vizio_portal/production/portal/index.html"),
            "chromium-html5-thelovedestination":(4,"57", "https://html5.thelovedestination.com/?ua=viziosmartcast"),
            "chromium-html5-pandora":(4,"58", "https://tv.pandora.com/?model=smartcast&vendor=vizio&type=HTML5&modelYear=2019&badge=vanambgxuwlwlrgdwmj4itmbf7oebk2fshibl464r33757w3itna"),
            "chromium-html5-cloudfrontindex":(4,"59","https://d1cu2xeuj8jvyz.cloudfront.net/vizio/prod/index.html"),
            "chromium-html5-cloudfrontsctv":(4,"60","https://dn6q4f0q0kh23.cloudfront.net/receiver/viziosmartcast/haystackreceiver.html?platform=sctv"),           
            #ColbaltApps
            "cobalt-youtube":(5,"1","https://www.youtube.com/tv"),
            "cobalt-youtubekids":(5,"2","https://www.youtube.com/tv_kids"),
            "cobalt-youtubetv":(5,"3","https://www.youtube.com/tv/upg"),
            "cobalt-youtubequale":(5,"4","https://qual-e.appspot.com/"),     
            #NativeApps
            "native-netflix":(3,"1",""),
            "native-usb":(3,"2",""),
            }

log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__))+'/Config')
AutoTestAppINI = log_file_path + '/AutoTestApp.INI'

restCfg = CfgParse(AutoTestAppINI)
dutIP = restCfg.GetCfgInfo("RestConnection","Ethernet.IP") #DUT IP Address
# print(("DUT IP address:",IP))
PORT=restCfg.GetCfgInfo("RestConnection","Port") # REST Port
# print(("REST Port:",PORT))
UDP_PORT=restCfg.GetCfgInfo("RestConnection","UDP_PORT") # REST Port
# print(("UDP Port:",UDP_PORT))
    

class Restkey_define(object):
    def __init__(self):
        pass
   
    def Rest_SingleKey_Play(self,key,pauseTimer):
        f_auth = open(Auth_Token,"r") #change
        auth_token = f_auth.readline().strip()
        HEADERS = {"auth": auth_token, "Content-Type": "application/json"} 
        
        if key in list(nommalKeyDict.keys()):
            print('Key:%s,%s,%s'%(key,nommalKeyDict.get(key)[0],nommalKeyDict.get(key)[1]))
            uri = "https://" + dutIP + ":" + PORT + "/key_command/"
            payload = json.dumps({"KEYLIST": [{"CODESET":int(nommalKeyDict.get(key)[0]),"CODE":int(nommalKeyDict.get(key)[1]),"ACTION":"KEYPRESS"}]})
            result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
            print(result)
            try: 
                if result["STATUS"]["RESULT"] != "SUCCESS":
                    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                    print("send signal again")
            except:
                pass
            time.sleep(pauseTimer)
        elif key in list(OTTKeyDict.keys()):
            print('Key:%s,NameSpace:%s,AppID:%s'%(key,OTTKeyDict.get(key)[0],OTTKeyDict.get(key)[1]))
            uri = "https://" + dutIP + ":" + PORT + "/app/launch"
            payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": int(OTTKeyDict.get(key)[0]), "APP_ID": OTTKeyDict.get(key)[1], "MESSAGE": OTTKeyDict.get(key)[2]}})
            result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
            print(result)
            try:
                if result["STATUS"]["RESULT"] != "SUCCESS":
                    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
            except:
                pass
            time.sleep(pauseTimer)      
        else:
            print("it's not defined key,please check it's in key list")        

    def Rest_GroupKeys_Play(self,fileInput):
        
        f_auth = open(Auth_Token,"r",encoding="UTF-8")
        auth_token = f_auth.readline().strip()
        HEADERS = {"auth": auth_token, "Content-Type": "application/json"}    
        
        folderName=fileInput.split(':')[0]
        fileName=fileInput.split(':')[1] 
        #shutil.copy2(folderName+'/'+fileName, 'execute.txt')
        
        
        try:
            
            if(os.path.exists("../execute.txt")):
                os.remove ('../execute.txt')

            f = open(folderName+'/'+fileName)
            shutil.copy2(folderName +'/' + fileName, '../execute.txt')
            f.close
            
        except IOError:
            print('File Name error or No such file or directory:%s'%(folderName+'/'+fileName))
    
                 
        if(os.path.exists("../execute.txt")):
              
            with open('../execute.txt') as f:
                for line in f:
                    #print (line)
                    if 'sleep' in line:
                        sleeptime=line.strip()[6:]
                        print(sleeptime)          
                        time.sleep(float(sleeptime))
                    else:
                        key=line.strip()
                                            
                        if key in list(nommalKeyDict.keys()):
                            print('Key:%s,%s,%s'%(key,nommalKeyDict.get(key)[0],nommalKeyDict.get(key)[1]))
                            uri = "https://" + dutIP + ":" + PORT + "/key_command/"
                            payload = json.dumps({"KEYLIST": [{"CODESET":int(nommalKeyDict.get(key)[0]),"CODE":int(nommalKeyDict.get(key)[1]),"ACTION":"KEYPRESS"}]})
                            result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                            print(result)
                            try:                      
                                if result["STATUS"]["RESULT"] != "SUCCESS":
                                    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                            except:
                                pass
                            #time.sleep(pauseTimer) 
                            #print result           
                         
                        elif key in list(OTTKeyDict.keys()):
                            print('Key:%s,NameSpace:%s,AppID:%s'%(key,OTTKeyDict.get(key)[0],OTTKeyDict.get(key)[1]))
                            uri = "https://" + dutIP + ":" + PORT + "/app/launch"
                            payload = json.dumps({"REQUEST": "MODIFY", "VALUE": {"NAME_SPACE": int(OTTKeyDict.get(key)[0]), "APP_ID": OTTKeyDict.get(key)[1], "MESSAGE": OTTKeyDict.get(key)[2]}})
                            result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                            #time.sleep(pauseTimer) 
                            print(result) 
                            try:   
                                if result["STATUS"]["RESULT"] != "SUCCESS":
                                    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                            except:
                                pass    
                        else:
                            print('The key %s not defined key,please check it in key list'%key)   
        else:
            print('Please check if the test case exist!')
              
         
if __name__ == "__main__":
    #key = "KEYBOARD_COMMA"
    #key = "KEYBOARD_Q"
    Rest = Restkey_define()
    #normal = Rest.Rest_SingleKey_Play(key,2)
    Rest.Rest_GroupKeys_Play("NetRatCaseSuite:NetRat_OOBE_7B.txt")


    
   
   
    
                
                
           

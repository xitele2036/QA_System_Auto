#!/usr/bin/python
#--*--coding:utf-8 --8--
#Connect virtual tablet

from appium import webdriver
import time
import requests
import json
from TestCfgParse import TestCfgParse
Auth_Token = "./Config/Auth_Token.txt"
castname = './Config/castname.txt'

GraphicWidgetDict={
                   "NetflixAccountSelection": "com.netflix.mediaclient:id/profile_avatar_img",
                   "NetflixCASTICON":"com.netflix.mediaclient:id/cast_icon_fab", 
                   "NetflixSearch": "com.netflix.mediaclient:id/search",
                   "NetflixSearchTextBox":"android:id/search_src_text",
                   "NetflixMovieSelection": "com.netflix.mediaclient:id/search_result_img",
                   "NetflixPlayButton": "com.netflix.mediaclient:id/video_play_icon",   
                   
                   "YoutubeCASTICON": "com.google.android.youtube:id/media_route_button",
                   "YoutubeSearchTextBox": "com.google.android.youtube:id/search_edit_text",
                   "YoutubeSearchResult": "com.google.android.youtube:id/text",
                   "YoutubePlayButton": "com.google.android.youtube:id/play_text",
                   "YoutubeSearchButton": "com.google.android.youtube:id/menu_item_1",
                   }
castDeviceName=''
castDeviceModel=''
castCfg=TestCfgParse()
IP=castCfg.GetTestCfgInfo("Ethernet.IP")
# print(("DUT IP address:",IP))
PORT=castCfg.GetTestCfgInfo("Port")
# print(("REST Port:",PORT))
DICT_FILE=castCfg.GetTestCfgInfo("DICT_FILE")
# print(("Dictionary File:",DICT_FILE))
Tablet_IP=castCfg.GetTestCfgInfo("Tablet_IP")
print(("Tablet_IP:",Tablet_IP))
castDeviceName=castCfg.GetTestCfgInfo("CAST_DEVICE_NAME")
print('You are using %s'%(castDeviceName)) 
castDeviceModel=castCfg.GetTestCfgInfo("CAST_DEVICE_MODEL")
print('You are using %s'%(castDeviceModel)) 

class Tablet_Cast_Test(object):
    def __init__(self):
        pass
    def appButtonClick(self,GButton,pauseTime):
        print("Button click funtion")   
        if GButton in list(GraphicWidgetDict.keys()):
            print("reserved")
            print(GButton)
            print(GraphicWidgetDict.get(GButton))
            print(pauseTime)
            print('resourceId=%s'%GraphicWidgetDict.get(GButton))
            print('new UiSelector().resourceId("'+GraphicWidgetDict.get(GButton)+'")')
            self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId(\"'+GraphicWidgetDict.get(GButton)+'\")').click()
            time.sleep(int(pauseTime))
    
    def appDescriptionButtonClick(self,text,pauseTime):
        print("DiscriptionButtion click function")
        self.driver.find_element_by_android_uiautomator('new UiSelector().descriptionContains(\"'+text+'\")').click()     

    def appTextClick(self,Text,pauseTime):
        self.driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+Text+'\")').click()
        time.sleep(pauseTime)
    
    def appTextSend(self,GButton,Text,pauseTime):
        if GButton in list(GraphicWidgetDict.keys()):
            self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId(\"'+GraphicWidgetDict.get(GButton)+'\")').send_keys(Text)
            time.sleep(int(pauseTime))
        else:
            print("The virtual key not defined")  
    
    def install_app(self):
        self.driver.install_app('path/to/my.apk')
        
    def uninstall_app(self):
        self.driver.remove_app('com.example.android.apis')
        
    def reset_app(self):
        self.driver.resetApp()
    
    def Get_Castname(self):
        try:
            f_auth = open(Auth_Token,"r")
            auth_token = f_auth.readline().strip()
            uri = "https://" + IP + ":" + PORT + "/menu_native/dynamic/tv_settings/system/system_information/tv_information/cast_name"
            result_json = requests.get(uri, verify=False, headers={"AUTH": auth_token}).json()
            print((json.dumps(result_json, indent=4, separators=(',', ': '))))
            cast_name = result_json["ITEMS"][0]["VALUE"]
            print(cast_name)
            f_castname = open(castname,"w")
            f_castname.write(cast_name)         
            return cast_name
        except:
            print("can't get casename,please check rest function work normally")
            
    def Cast_Netflix(self,movie,pauseTime):
        desired_caps = {
                        'platformName': 'Android',
                        'platformVersion': '6.0.1',
                        'deviceName': '10.86.79.40:5555',
                        'appPackage': 'com.netflix.mediaclient',
                        'appActivity': '.ui.launch.UIWebViewActivity',
                        'unicodeKeyboard': 'True',
                        'resetKeyboard': 'True',
                        'noReset': 'True'
                        }          
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
        print((self.driver.is_app_installed(NetflixappPackage)))
        size = self.driver.get_window_size()
        print(size)
        try:
            self.driver.close_app()
            time.sleep(10)
            self.driver.launch_app()
            time.sleep(10)
            self.appButtonClick("NetflixAccountSelection",5)
            self.appButtonClick("NetflixCASTICON",5)
            with open(castname,"r") as f: 
                castname = f.read().strip()   
                print(castname)           
            self.appTextClick(castname,5)
            self.appButtonClick("NetflixSearch",5)
            self.appTextSend("NetflixSearchTextBox",movie,5)
            self.appButtonClick("NetflixMovieSelection",5)
            self.appButtonClick("NetflixPlayButton",pauseTime)
        except:
            print("Please check Netflix cast function")
    
    def Cast_Youtube(self,movie,pauseTime):
        desired_caps = {
                        'platformName': 'Android',
                        'platformVersion': '6.0.1',
                        'deviceName': '10.86.79.40:5555',
                        'appPackage': 'com.google.android.youtube',
                        'appActivity': 'com.google.android.apps.youtube.app.WatchWhileActivity',
                        'unicodeKeyboard': 'True',
                        'resetKeyboard': 'True',
                        'noReset': 'True'
                        }
        
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
        size = self.driver.get_window_size()
        print(size)
        print((self.driver.is_app_installed("com.google.android.youtube")))
        try:
            
            self.driver.close_app()
            time.sleep(3)
            self.driver.launch_app()
            time.sleep(5)     
            self.appButtonClick("YoutubeCASTICON",5)
            with open(castname,"r") as f: 
                castname = f.read().strip()   
                print(castname)  
            self.appTextClick(castname,5)   
            self.appButtonClick("YoutubeSearchButton",5)
            self.appTextSend("YoutubeSearchTextBox",movie,5)
            self.appButtonClick("YoutubeSearchResult",5)
            self.appDescriptionButtonClick(movie,5)
            self.appButtonClick("YoutubePlayButton",pauseTime)     
        except:
            print("Exit cast youtube progress and please check if something wrong!")
        
"""       
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.google.android.youtube:id/media_route_button")').click()
        time.sleep(5)
        driver.find_element_by_android_uiautomator('new UiSelector().text("00")').click()
        time.sleep(5)
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.google.android.youtube:id/menu_item_1")').click()
        time.sleep(5)
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.google.android.youtube:id/search_edit_text")').send_keys("The world in HDR in 4k")
        time.sleep(5)
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.google.android.youtube:id/text")').click()
        time.sleep(5)
        #movie="The World in HDR in 4K (ULTRA HD) - 2 minutes, 35 seconds -  - Jacob + Katie Schwarz - 16M views - 3 years ago - play video"
        driver.find_element_by_android_uiautomator('new UiSelector().description("The World in HDR in 4K (ULTRA HD) - 2 minutes, 35 seconds -  - Jacob + Katie Schwarz - 16M views - 3 years ago - play video")').click()
        time.sleep(6)
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.google.android.youtube:id/play_text")').click()
        time.sleep(15)    
"""        
if __name__ == '__main__':
    #NetflixappPackage = 'com.netflix.mediaclient'
    #NetflixappActivity = '.ui.launch.UIWebViewActivity'
    #YoutubeappPackage = 'com.google.android.youtube'
    #YoutubeappActivity = 'com.google.android.apps.youtube.app.WatchWhileActivity'
    #movie = 'marco polo'
    movie = 'The World in HDR in 4K '
    pauseTime = '30'
    #DEVICE_NAME = '10.86.79.40:5555'
    My_tablet_Cast = Tablet_Cast_Test()
    My_Cast_Device = My_tablet_Cast.Get_Castname()
    #My_Netflix_Cast = My_tablet_Cast.Cast_Netflix(NetflixappPackage,NetflixappActivity,movie,pauseTime)
    My_Youtube_Cast = My_tablet_Cast.Cast_Youtube(movie,pauseTime)
   

    






    


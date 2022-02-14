#!/usr/bin/python
#--*--coding:utf-8 --8--
#Connect virtual tablet
import uiautomator2 as u2
from time import sleep
import re
import requests
import json
from modules.TestCfgParse import TestCfgParse
Auth_Token = "./Config/Auth_Token.txt"
castname = './Config/castname.txt'
#In development
GraphicWidgetDict={
                   "NetflixCASTICON":"com.netflix.mediaclient:id/cast_icon_fab", 
                   "NetflixBACK":'com.netflix.mediaclient:id/menu_navigation_button_view',  
                   "NetflixSearch_Nexus":"com.netflix.mediaclient:id/ab_menu_search_item",
                   "NetflixSearch_Vizio": "com.netflix.mediaclient:id/label", #need to add text is "Search"
                   "NetflixSearchTextBox":"android:id/search_src_text",
                   "NetflixPlayButton": "com.netflix.mediaclient:id/video_play_icon",
                   "NetflixPauseButton_Nexus": "com.netflix.mediaclient:id/player_pause_btn",
                   "NetflixMiniBarToggle_Nexus": "com.netflix.mediaclient:id/cast_player_text_group_caret",
                   "NetflixMiniBarToggle_Vizio": "com.netflix.mediaclient:id/caret",
                   "NetflixHomeButton": "com.netflix.mediaclient:id/icon",
                   "NetflixHomePagePlayButton_Nexus": "com.netflix.mediaclient:id/billboard_cta1_button",
                   "NetflixReadyStopCastIcon_Nexus": "com.netflix.mediaclient:id/cast_player_device_name_group",
                   "NetflixReadyStopCastIcon_Vizio": "com.netflix.mediaclient:id/cast",
                   "NetflixDeleteSearchMovie_Vizio": "android:id/search_close_btn", #delete search movie
                   
                   "DisneySearchTextBox": "com.disney.disneyplus:id/search_src_text",
                   
                   "YoutubeHomeButton": "com.google.android.youtube:id/text",
                   "YoutubeCASTICON": "com.google.android.youtube:id/media_route_button",
                   "YoutubeSearch": "Search", #description
                   "YoutubeSearchConfirm": "com.google.android.inputmethod.pinyin:id/icon",
                   "YoutubeSearchTextBox": "com.google.android.youtube:id/search_edit_text",
                   "YoutubeMiniBarToggle": "com.google.android.youtube:id/minibar_title",
                   "YoutubePlayButton": "com.google.android.youtube:id/play_text",
                   "YoutubePlayPauseButton_Nexus": "com.google.android.youtube:id/play_pause",
                   "YoutubeCollapseButton": "com.google.android.youtube:id/player_collapse_button",
                   "YoutubeFloatCloseButton_Vizio": "com.google.android.youtube:id/floaty_close_button",
                   "YoutubeSearchBack": "Navigate up",  #description
                   "YoutubeStopCast": "android:id/button1",
                   
                   "HuluCASTICON": "Cast button. Disconnected",  #description
                   "HuluPlayButtion": "com.hulu.plus:id/play_button",
                   "HuluSearch": "com.hulu.plus:id/menu_search",
                   "HuluSearchTextBox": "com.hulu.plus:id/search_src_text",
                   "HuluMovieSelect": "com.hulu.plus:id/tile_title",
                   "HuluPlayButton": "com.hulu.plus:id/start_watching_button_text",
                   "HuluStopCastButton": "android:id/button1",
                   "HuluBack": "Navigate up",
                   
                   "DisneyHomeButton": "com.disney.disneyplus:id/menuIcon",
                   "DisneyCASTICON": "com.disney.disneyplus:id/castButton",
                   "DisneyMovieSelection": "com.disney.disneyplus:id/title",
                   "DisneyPlayButton": "com.disney.disneyplus:id/bookMarkIcon",
                   "DisneyStopCast": "android:id/button1",
                   "DisneyBackKey": "com.disney.disneyplus:id/blackBackButton",
                   
                   "PlayMusicSearch": "com.google.android.music:id/search",
                   "PlayMusicSearchTextBox": "com.google.android.music:id/search_box_text_input",
                   "PlayMusicSearchResult": "com.google.android.music:id/suggest_text",
                   "PlayMusicPlayButton": "com.google.android.music:id/fab_play",
                   "PlayMusicStopCast": "android:id/button1"
                   }
              
ImageWidgetDict={
                "NetflixMovieSelection_NEXUS": "com.netflix.mediaclient:id/search_result_img", 
                #"NetflixMovieSelection_Vizioorg": "com.netflix.mediaclient:id/movie_boxart",
                "NetflixMovieSelection_Vizio": "com.netflix.mediaclient:id/search_result_img",
                "NetflixAccountSelection": "com.netflix.mediaclient:id/profile_avatar_img", #main account selection
                "NetflixTDSelection": "com.netflix.mediaclient:id/movie_boxart",  #TV Drammas first video
                "NetflixCWSelection": "com.netflix.mediaclient:id/cw_view_img"  #Continue Watching
                }
DescriptionWidgetDict={
                "YoutubeSearch": "Search", 
                "YoutubeSearchBack": "Navigate up",  
                "HuluCASTICON": "Cast button. Disconnected",  
                "HuluStopCASTICON": "Cast button. Connected",
                "DisneyCASTICON_Eng": "Cast button. Connected",
                "DisneyCASTICON_Chi": "投射按钮。已连接",
                "PlayMusicCASTICON_Chi": "投射按钮。已断开连接",
                "PlayMusicSTOPSCASTICON_Chi": "投射按钮。已连接",
                
                }

OTT=''  
castDeviceModel=''
castCfg=TestCfgParse()
IP=castCfg.GetTestCfgInfo("Ethernet.IP")
# print(("DUT IP address:",IP))
PORT=castCfg.GetTestCfgInfo("Port")
# print(("REST Port:",PORT))
DICT_FILE=castCfg.GetTestCfgInfo("DICT_FILE")
# print(("Dictionary File:",DICT_FILE))
castDeviceModel=castCfg.GetTestCfgInfo("CAST_DEVICE_MODEL")
print('You are using %s'%(castDeviceModel))   


class Tablet_Cast_Test(object):

    def __init__(self):
        pass
    
    def Device_Connect(self):
        tablet_ip=castCfg.GetTestCfgInfo("Tablet_IP")
        print(("Cast Device IP Address:",tablet_ip))
        
        self.d = u2.connect(tablet_ip)
            
        if self.d.info.get('screenOn')==False:
            self.d.screen_on()
            self.d.unlock()        
    
        print(self.d.info)
        print("Please start uiautomator2 on your test PC if it's not yet started")
        sleep(5)
        
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
    
    def appButtonClick(self,GButton,pauseTime):
        print("Button click funtion")
        
        if GButton in list(GraphicWidgetDict.keys()):
            print("reserved")
            print(GButton)
            print(GraphicWidgetDict.get(GButton))
            print(pauseTime)
            print('resourceId=%s'%GraphicWidgetDict.get(GButton))
            self.d(resourceId=GraphicWidgetDict.get(GButton)).click()
            sleep(int(pauseTime))
        elif GButton in list(ImageWidgetDict.keys()):
            print(GButton)
            print(ImageWidgetDict.get(GButton))
            print(pauseTime)
            print('resourceId=%s'%ImageWidgetDict.get(GButton))
            self.d(resourceId=ImageWidgetDict.get(GButton)).click()
            sleep(int(pauseTime))
        else:
            print("The virtual key not defined")
            
    def DescriptionButtonClick(self, DButton,pauseTime):
        if DButton in list(DescriptionWidgetDict.keys()):
            print(DButton)
            print(DescriptionWidgetDict.get(DButton))
            print(pauseTime)
            self.d(description=DescriptionWidgetDict.get(DButton)).click()
            sleep(int(pauseTime))   
        else:
            print("description button isn't defined")            
            
    def appButtonPress(self,GButton,pauseTime):
        self.d.press(GButton)
        sleep(pauseTime)

    def appTextClick(self,Text,pauseTime):
        self.d(text=Text).click()
        sleep(pauseTime)
    def appTextWait(self,Text,pauseTime):
        self.d(text=Text).wait(timeout=pauseTime)
    
    def appTextScroll(self,Text,pauseTime):
        self.d(scrollable=True).scroll.to(text=Text)
        sleep(pauseTime)
        
    def appTextSend(self,GButton,Text,pauseTime):
        if GButton in list(GraphicWidgetDict.keys()):
            self.d(resourceId=GraphicWidgetDict.get(GButton)).send_keys(Text)
            sleep(int(pauseTime))
        else:
            print("The virtual key not defined")        
 #Cast Init   
    def Cast_Test_Init(self):
        try:
            self.Device_Connect()
        except:
            print("Device connection failed, please check python -m uiautomator command is running")
            
        TableDevN = self.Get_Castname()
        Status = 1
        
        if self.d.info.get('screenOn')==False:
            self.d.screen_on()
            self.d.unlock()   
        self.appButtonPress("home",2)
        print("press home key")
        
    def Cast_OTT_Launch(self,OTT):
        try: 
            self.appTextClick(OTT,8)
            print("OTT key is pressed and launched")
        except:
            print("Check the test OTT is in first page of your device")
    
    def CastName_Click(self): 
        with open(castname,"r") as f: 
            castname = f.read().strip()   
            print(castname)
        try:
            #if self.appTextWait(castname,8.0)==True:
            if self.d(text=castname).wait(timeout=10.0) == True: 
                self.appTextClick(castname,15)  # Select the DUT's Name
            else:
                self.appTextScroll(castname,3)
                self.appTextClick(castname,15)   
                print("select device name successfully")
        except:
            print("The DUT cast name can't be found")
            sleep(20)
            
# Cast Netflix Test       
    def NetflixCast_Icon_Click(self):
        #if self.appTextWait("Who's Watching?",10.0)==True:
        if self.d(resourceId="com.netflix.mediaclient:id/profile_selection_title", text="Who's Watching?").wait(timeout=10.0) == True:
            print("who's watching")
            self.appButtonClick("NetflixAccountSelection",2)
            self.appButtonClick("NetflixCASTICON",3) #click CAST icon
        else:
            self.appButtonClick("NetflixCASTICON",3) #Click CAST icon  
            print("Click Netflix Cast Icon successfully")
                    
    def Cast_Netflix_movieSearch(self,movie):
        if castDeviceModel=="Vizio_tablet":
            print(castDeviceModel)
            self.appTextClick("Search",5)
            self.appButtonClick("NetflixSearchTextBox",5)
            if self.d(text="Netflix").wait(timeout=5.0)==True:  
                self.appTextClick("Netflix",5)
            else:
                print("input movie name directly")
            self.appTextSend("NetflixSearchTextBox",movie,3)
            self.appButtonClick("NetflixMovieSelection_Vizio",2)
        elif castDeviceModel=="NEXUS_tablet":
            self.appButtonClick("NetflixSearch_Nexus",2)
            self.appButtonClick("NetflixSearchTextBox",2)
            self.appTextSend("NetflixSearchTextBox",movie,2)
            self.appButtonClick("NetflixMovieSelection_NEXUS",2)
        else:
            print("can't find your selected movie")
            
    def Netflix_moviePlayback(self,pauseTime):
        print("it start to playback")
        try:
            self.appButtonClick("NetflixPlayButton",pauseTime)
        except:
            pass
            
    def Disconnect_Netflix_Cast(self):
        if castDeviceModel=="NEXUS_tablet":
            self.appButtonClick("NetflixMiniBarToggle_Nexus",3)
            self.appButtonClick("NetflixReadyStopCastIcon_Nexus",3)
            self.appTextClick("Disconnect",4)
        elif castDeviceModel=="Vizio_tablet":
            self.appButtonClick("NetflixMiniBarToggle_Vizio",3)
            self.appButtonClick("NetflixReadyStopCastIcon_Vizio",3)
            self.appTextClick("Disconnect",4)   
        else:
            print("can't disconnect device")
            
    def Netflix_Test_Finish(self):
        if castDeviceModel=="NEXUS_tablet":
            self.appButtonClick("NetflixBACK",3)
            self.appButtonClick("NetflixBACK",2)
            print("Cast Netflix with NEXUS tablet finish")
        elif castDeviceModel=="Vizio_tablet":
            self.appButtonClick("NetflixBACK",3)
            self.appButtonClick("NetflixHomeButton",2)
            print("Cast Netflix with Vizio tablet finish")
        else:
            print("Please check Netflix app status")
                       
    def Cast_Netflix(self,OTT,movie,pauseTime):
        try:
            self.Cast_Test_Init()
            self.Cast_OTT_Launch(OTT)
            self.NetflixCast_Icon_Click()
            self.CastName_Click()
            self.Cast_Netflix_movieSearch(movie)
            self.Netflix_moviePlayback(pauseTime)
            self.Disconnect_Netflix_Cast()
            self.Netflix_Test_Finish()
        except:
            print("can't excute cast netflix test successfully")
        
#Cast Youtube Test
    def YoutubeCast_Icon_Click(self):
        try:
            self.appButtonClick("YoutubeHomeButton",5)
            print("Click youtube cast icon")
            self.appButtonClick("YoutubeCASTICON",3)
        except:
            print("can't find youtube cast icon")
            
    def Cast_Youtube_movieSearch(self,movie):
        try:
            self.appTextClick("Library",3)
            try:
                if self.d(text="Auto test stream").wait(timeout=10.0) == True: 
                    self.appTextClick("Auto test stream",5)  # Select Auto test stream library
                else:
                    self.appTextScroll("Auto test stream",3)
                    self.appTextClick("Auto test stream",5)   
                    print("select device name successfully")
            except:
                print("Auto test stram library can't be found")            
            #self.appTextClick("Auto test stream",5)
            self.appTextClick(movie,5)
        except:
            print("Please check the video in Auto test stream library")
            
    def Youtube_VideoPlayback(self,pauseTime):
        print("it start to playback youtube")
        self.appButtonClick("YoutubePlayButton",pauseTime)
    
    def Disconnect_Youtube_Cast(self):
        try:
            self.appButtonClick("YoutubeMiniBarToggle",2)
            self.appButtonClick("YoutubeCASTICON",3)
            self.appButtonClick("YoutubeStopCast",5)
        except:
            print("Stop casting youtube failed")
            
    def Youtube_Test_Finish(self):
        if castDeviceModel=="Vizio_tablet":
            self.appButtonClick("YoutubeCollapseButton",4)
            self.appButtonClick("YoutubeFloatCloseButton_Vizio",3)
            self.DescriptionButtonClick("YoutubeSearchBack",5)
        elif castDeviceModel=="NEXUS_tablet":
            self.appButtonClick("YoutubeCollapseButton",4)
            print("*********")
            self.d.swipe(0.612, 0.819,0.983, 0.809)
            #self.DescriptionButtonClick("YoutubeSearchBack",5)       
        else:
            print("can't recover youtube to init status")
    
    def Cast_Youtube(self,OTT,movie,pauseTime):
        try:
            self.Cast_Test_Init()
            self.Cast_OTT_Launch(OTT)
            self.YoutubeCast_Icon_Click()
            self.CastName_Click()
            self.Cast_Youtube_movieSearch(movie)
            self.Youtube_VideoPlayback(pauseTime)
            self.Disconnect_Youtube_Cast()
            self.Youtube_Test_Finish()
        except:
            print("Can't execute cast youtube test successfully")

#Cast Disney+
    def DisneyCast_Icon_Click(self):
        try:
            self.appTextClick("Home",5)
            print("Click Disney cast icon")
            self.appButtonClick("DisneyCASTICON",3)
        except:
            print("can't find Disney cast icon")

    def Cast_Disney_movieSearch(self,movie):
        try:
            self.appTextClick("Search",3)
            self.appButtonClick("DisneySearchTextBox",2)
            self.appTextSend("DisneySearchTextBox",movie,2)
            self.appTextClick(movie,5)
        except:
            print("Please check disney search function")

    def Disney_VideoPlayback(self,pauseTime):
        try: 
            self.appButtonClick("DisneyPlayButton",pauseTime)
            print("it starts to play Disney movie")
        except:
            print("can't playback disney movie correctly")
    
    def Disconnect_Disney_Cast(self):
        try:
            self.DescriptionButtonClick("DisneyCASTICON_Chi",3)
            self.appButtonClick("DisneyStopCast",5)
        except:
            print("Stop casting Disney failed")    

    def Disney_Test_Finish(self):
        try:
            self.appTextClick("Home",3)
        except:
            print("DisneyPlus return to home page failed")    
        
            
    def Cast_DisneyPlus(self,OTT,movie,pauseTime):
        try:
            self.Cast_Test_Init()
            self.Cast_OTT_Launch(OTT)
            self.DisneyCast_Icon_Click()
            self.CastName_Click()
            self.Cast_Disney_movieSearch(movie)
            self.Disney_VideoPlayback(pauseTime)
            self.Disconnect_Disney_Cast()
            self.Disney_Test_Finish()
        except:
            print("Cast DisneyPlus work incorrectly")
            
#Cast Google PlayMusic            
    def Cast_PlayMusic(self,OTT,movie,pauseTime):
        try:
            self.Cast_Test_Init()
            self.Cast_OTT_Launch(OTT)
            self.PlayMusicCast_Icon_Click()
            self.CastName_Click()
            self.Cast_PlayMusic_movieSearch(movie)
            self.PlayMusic_VideoPlayback(pauseTime)
            self.Disconnect_PlayMusic_Cast()
            #self.PlayMusic_Test_Finish()
        except:
            print("Cast PlayMusic work incorrectly")    
    
    def PlayMusicCast_Icon_Click(self):
        try:
            self.DescriptionButtonClick("PlayMusicCASTICON_Chi",3)
        except:
            print("can't find PlayMusic cast icon")    
            
    def Cast_PlayMusic_movieSearch(self,movie):
        try:
            self.appButtonClick("PlayMusicSearch",3)
            self.appButtonClick("PlayMusicSearchTextBox",3)
            self.appTextSend("PlayMusicSearchTextBox",movie,3)
            self.appButtonClick("PlayMusicSearchResult",5)
        except:
            print("Please check PlayMusic search function")    
            
    def PlayMusic_VideoPlayback(self,pauseTime):
        try: 
            self.appButtonClick("PlayMusicPlayButton",pauseTime)
            print("it starts to play Disney movie")
        except:
            print("can't playback PlayMusic correctly") 
            
    def Disconnect_PlayMusic_Cast(self):
        try:
            self.DescriptionButtonClick("PlayMusicSTOPSCASTICON_Chi",3)
            self.appButtonClick("PlayMusicStopCast",5)
        except:
            print("Stop casting PlayMusic failed")       
            
        
#Cast Hulu Test
    def HuluPlusCast_Icon_Click(self):
        try:
            print("Click Hulu cast icon")
            self.DescriptionButtonClick("HuluCASTICON",3)
        except:
            print("can't find hulu cast icon")
                       
    def Cast_HuluPlus_MovieSearch(self,movie):
        try:
            self.appButtonClick("HuluSearch",3)
            self.appButtonClick("HuluSearchTextBox",2)
            self.appTextSend("HuluSearchTextBox",movie,2) 
            try:
                #self.appTextClick(movie,10)
                self.appButtonClick("HuluMovieSelect",8)
            except: 
                print("can't search your hulu video to play")
        except:
            print("Please input correct video to search")   
            
    def HuluPlus_VideoPlayback(self,pauseTime):
        #if Status==1:
        print("it start to playback Hulu")
        self.appButtonClick("HuluPlayButton",pauseTime)

    def Disconnect_HuluPlus_Cast(self):
        try:
            self.DescriptionButtonClick("HuluStopCASTICON",3)
            self.appButtonClick("HuluStopCastButton",5)
        except:
            print("Stop casting Hulu failed")
    
    def Cast_Hulu(self,OTT,movie,pauseTime):
        try:
            self.Cast_Test_Init()
            self.Cast_OTT_Launch(OTT)
            self.HuluPlusCast_Icon_Click()
            self.CastName_Click()
            self.Cast_HuluPlus_MovieSearch(movie)
            self.HuluPlus_VideoPlayback(pauseTime)
            self.Disconnect_HuluPlus_Cast()
        except:
            print("can't excute cast hulu test successfully")

if __name__ == '__main__':
    #OTT = 'Netflix'
    #movie = 'Test Patterns'
    #movie = 'Marco polo'
    #pauseTime = '60'
    
    #OTT = 'YouTube'
    #movie = 'Men in Black 3'
    #pauseTime = '60'
    
    #OTT = 'Hulu'
    #movie = 'The Bachelorette'
    #pauseTime = '60'
    
    #OTT = 'Disney+'
    #movie = 'Frozen'
    #pauseTime ='60'
    
    OTT = 'Play 音乐'
    movie = 'The WOJ Pod'
    pauseTime = '60'
    
    My_tablet_Cast = Tablet_Cast_Test()
    #My_Netflix_Cast = My_tablet_Cast.Cast_Netflix(OTT,movie,pauseTime)
    #My_Youtube_Cast = My_tablet_Cast.Cast_Youtube(OTT,movie,pauseTime)
    #My_HuluPlus_Cast = My_tablet_Cast.Cast_Hulu(OTT,movie,pauseTime)
    #My_DisneyPlus_Cast = My_tablet_Cast.Cast_DisneyPlus(OTT,movie,pauseTime)
    My_PlayMusic_Cast =  My_tablet_Cast.Cast_PlayMusic(OTT,movie,pauseTime)
    
   
   
 
    
 
    
        
        
        
        
            
            
            
            
    
    
    
    
    
    
    

   


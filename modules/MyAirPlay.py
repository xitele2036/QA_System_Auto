import requests

from airtest.core.api import *
from poco.drivers.ios import iosPoco
from modules.MyReFiler import ReFilter
from modules.log import logger
import subprocess
from modules.ssh_utility_asyncssh import CapLogcat
from modules.TestCfgParse import TestCfgParse


AirplayCfg = TestCfgParse()
IP = AirplayCfg.GetTestCfgInfo('Ethernet.IP')
PORT=AirplayCfg.GetTestCfgInfo("Port")
Auth_Token = "./Config/Auth_Token.txt"
castname = './Config/castname.txt'




class APP():

    def APPlaunch(self, status, appname):
        try:
            if "start" == status:
                if "YouTube" == appname:
                    subprocess.check_output("tidevice launch com.google.ios.youtube")
                elif "hulu" == appname:
                    subprocess.check_output("tidevice launch com.hulu.plus")
                elif "vudu" == appname:
                    subprocess.check_output("tidevice launch com.vudu.VuduIosClient")
                elif "amazon" == appname:
                    subprocess.check_output("tidevice launch com.amazon.aiv.AIVApp")
                elif "Disney" == appname:
                    subprocess.check_output("tidevice launch com.disney.disneyplus")
                elif "Netflix" == appname:
                    subprocess.check_output("tidevice launch com.netflix.Netflix")
                elif "AppleTV" == appname:
                    subprocess.check_output("tidevice launch com.apple.tv")
                else:
                    logger.info("Not found " + appname)
            else:
                if "YouTube" == appname:
                    subprocess.check_output("tidevice kill com.google.ios.youtube")
                elif "hulu" == appname:
                    subprocess.check_output("tidevice kill com.hulu.plus")
                elif "vudu" == appname:
                    subprocess.check_output("tidevice kill com.vudu.VuduIosClient")
                elif "amazon" == appname:
                    subprocess.check_output("tidevice kill com.amazon.aiv.AIVApp")
                elif "Disney" == appname:
                    subprocess.check_output("tidevice kill com.disney.disneyplus")
                elif "Netflix" == appname:
                    subprocess.check_output("tidevice kill com.netflix.Netflix")
                elif "AppleTV" == appname:
                    subprocess.check_output("tidevice kill com.apple.tv")
                else:
                    logger.info("Not found " + appname)
            sleep(10)
            print("Close " + appname)
        except Exception as e:
            print(e.args)
            logger.info("Not found " + appname)


class AIRPLAY():

    def __init__(self):
        connect_device("iOS:///127.0.0.1:8100")
        self.poco = iosPoco()
        self.log_file_path = os.path.realpath("/IOS/IOS-TEST/log/")
        self.L = CapLogcat(IP)
        self.TVname = self.Get_Castname()


    def Get_Castname(self):
        try:
            f_auth = open(Auth_Token,"r")
            auth_token = f_auth.readline().strip()
            uri = "https://" + IP + ":" + PORT + "/menu_native/dynamic/tv_settings/system/system_information/tv_information/cast_name"
            result_json = requests.get(uri, verify=False, headers={"AUTH": auth_token}).json()
            # print((json.dumps(result_json, indent=4, separators=(',', ': '))))
            cast_name = result_json["ITEMS"][0]["VALUE"]
            print(cast_name)
            f_castname = open(castname,"w")
            f_castname.write(cast_name)
            return cast_name
        except:
            print("can't get casename,please check rest function work normally")


    def APPlaunch(self, status, appname):
        try:
            if "start" == status:
                if "YouTube" == appname:
                    start_app("com.google.ios.youtube")
                elif "hulu" == appname:
                    start_app("com.hulu.plus")
                elif "vudu" == appname:
                    start_app("com.vudu.VuduIosClient")
                elif "amazon" == appname:
                    start_app("com.amazon.aiv.AIVApp")
                elif "Disney" == appname:
                    start_app("com.disney.disneyplus")
                elif "Netflix" == appname:
                    start_app("com.netflix.Netflix")
                elif "AppleTV" == appname:
                    start_app("com.apple.tv")
                else:
                    logger.info("Not found " + appname)
            else:
                if "YouTube" == appname:
                    stop_app("com.google.ios.youtube")
                elif "hulu" == appname:
                    stop_app("com.hulu.plus")
                elif "vudu" == appname:
                    stop_app("com.vudu.VuduIosClient")
                elif "amazon" == appname:
                    stop_app("com.amazon.aiv.AIVApp")
                elif "Disney" == appname:
                    stop_app("com.disney.disneyplus")
                elif "Netflix" == appname:
                    stop_app("com.netflix.Netflix")
                elif "AppleTV" == appname:
                    stop_app("com.apple.tv")
                else:
                    logger.info("Not found " + appname)
                print("Close " + appname)
            sleep(10)

        except Exception as e:
            print(e.args)
            logger.info("Not found " + appname)


    def Home(self):
        keyevent("home")

    def netflixuser(self):
        try:
            # print(self.poco('tester_vvv@netflix.com').wait(5).exists())
            if self.poco('tester_vvv@netflix.com').wait(5).exists():
                # touch(Template(r"netflix\netflixuser.png",target_pos=5))
                self.poco("tester_vvv@netflix.com").wait(3).click()
            else:
                logger.info("Already logged in Netflix")
                # snapshot(self.log_file_path + '\{0}-Already logged in Netflix.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')), quality=30)
        except Exception as e:
            print(e.args)
            print("can't login netflix fail")
            # snapshot(
            #     self.log_file_path + '\{0}-Netflix loggin fail.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')),
            #     quality=30)

    def netflixcast(self,Movie,Time):
        # if self.poco('tester_vvv@netflix.com').wait(5).exists():
        #     # touch(Template(r"netflix\netflixuser.png",target_pos=5))
        #     self.poco("tester_vvv@netflix.com").wait(3).click()
        # sleep(10)


        try:
            self.poco("mdxButton-Available").wait(3).click()
            sleep(10)
            print(self.poco(self.TVname).get_position())
            self.poco(self.TVname).wait(3).click('center')
            sleep(10)
            self.poco("searchButton").wait(3).click()
            text(Movie)
            self.poco("81045007-My Octopus Teacher-movie-loaded").wait(5).click()
            self.poco("playButton").wait(3).click()
            sleep(3)
            self.poco("homeTab").wait(3).click()
            sleep(3)
            self.poco("homeTab").wait(3).click()
            sleep(int(Time))
            self.poco("mdxButton-CastSessionInProgress").wait(3).click()
            self.poco("Disconnect").wait(3).click()
        except Exception as e:
            print(e.args)
            print("netflix cast execute fail")
            # snapshot(
            #     self.log_file_path + '\{0}-Netflix cast execute fail.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')),
            #     quality=30)

    def youtubecast(self,Movie,Time):
        try:
            self.poco("id.mdx.playbackroute.button").wait(3).click()
            sleep(5)
            self.poco("id.mdx."+self.TVname+".connect.button").wait(3).click()
            sleep(5)
            self.poco("id.ui.navigation.search.button").wait(3).click()
            text(Movie)
            # touch(Template(r"youtube\the_world_in_hdr_in_4k.png", target_pos=5))
            self.poco("Window").child("Other").offspring("id.app.view").\
                child("Other")[0].child("Other").offspring("Top View").\
                child("Other")[1].child("Other").child("Other").\
                offspring("CollectionView").child("Cell")[1].\
                child("Other").child("eml.cvr").child("eml.cvr").wait(3).click()
            sleep(3)
            if self.poco('Play').wait(3).exists():
                self.poco("Play").wait(3).click()
            sleep(int(Time))
            # touch(Template(r"youtube\youtubeplay.png", target_pos=5))
            self.poco("id.mdx.playbackroute.button").wait(3).click()
            self.poco("DISCONNECT").wait(3).click()
        except Exception as e:
            print(e.args)
            print("youtube cast execute fail")
            # snapshot(
            #     self.log_file_path + '\{0}-Youtube cast execute fail.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')),
            #     quality=30)

    def appletvairplay(self,Movie,Time):
        sleep(5)
        try:
            if exists(Template(r"../airplay/airplayico.png", target_pos=5)):
                self.poco("Search").wait(3).click()
                self.poco("Shows, Movies, and More").wait(3).click()
                text(Movie)
                sleep(10)
                self.poco(Movie).wait(3).click()
                self.poco("Resume").wait(3).click()
                sleep(int(Time))
                # self.poco("StaticText").wait(3).click()
                self.poco("Done").wait(3).click()
                sleep(3)
                self.poco("AirPlay").wait(3).click()
                # touch(Template(r"airplay\airplayico.png", target_pos=5))
                sleep(5)
                self.poco.wait_stable()
                self.poco("iPhone").wait(3).click()
                # touch(Template(r"airplay\playonipad.png", target_pos=5))
                sleep(5)
            else:
                self.poco("Search").wait(3).click()
                self.poco("Shows, Movies, and More").wait(3).click()
                text(Movie)
                sleep(10)
                self.poco(Movie).wait(3).click()
                self.poco("Resume").wait(3).click()
                self.poco("AirPlay").wait(3).click()
                sleep(5)
                self.poco(self.TVname).wait(3).click()
                # touch(Template(r"airplay\airplay.png", target_pos=5))
                sleep(3)
                self.L.capLog(10)
                mytxtfilter = ReFilter()
                code = mytxtfilter.getAirplayCode('./Logs/SSHlogcat.log')
                print(code.strip())
                text(code.strip())
                self.poco("OK").wait(3).click()
                sleep(3)
                touch([20,40])
                sleep(int(Time))
                # self.poco("StaticText").wait(3).click()
                # self.poco("Done").wait(3).click()
                sleep(3)
                self.poco("AirPlay").wait(3).click()
                # touch(Template(r"airplay\airplayico.png", target_pos=5))
                sleep(5)
                self.poco.wait_stable()
                self.poco("iPhone").wait(3).click()
                touch([20, 40])
                # touch(Template(r"airplay\playonipad.png", target_pos=5))
                sleep(5)
        except Exception as e:
            print(e.args)
            print("applytv airplay execute fail")
            # snapshot(
            #     self.log_file_path + '\{0}-Applytv airplay execute fail.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')),
            #     quality=30)



    def youtubeairplay(self,Movie,Time):
        try:
            self.poco("id.mdx.playbackroute.button").wait(3).click()
            print("Press Airplay Button")
            sleep(3)
            self.poco("id.mdx.AirPlay & Bluetooth devices.connect.button").wait(3).click()
            print("Press Airplay connect")
            sleep(5)
            self.poco(self.TVname).wait(3).click()
            # touch(Template(r"airplay\airplay.png", target_pos=5))
            print("TV name")
            self.L.capLog(10)
            mytxtfilter = ReFilter()
            code = mytxtfilter.getAirplayCode('./Logs/SSHlogcat.log')
            print(code.strip())
            text(code.strip())
            self.poco("OK").wait(3).click()
            sleep(3)
            touch([20,40])
            sleep(3)
            self.poco("id.ui.navigation.search.button").wait(3).click()
            print("Press search button")
            text(Movie)
            self.poco("Window").child("Other").offspring("id.app.view"). \
                child("Other")[0].child("Other").offspring("Top View"). \
                child("Other")[1].child("Other").child("Other"). \
                offspring("CollectionView").child("Cell")[1]. \
                child("Other").child("eml.cvr").child("eml.cvr").wait(10).click()
            sleep(3)
            # self.poco("Play").wait(3).click()
            sleep(int(Time))
            self.poco("id.mdx.playbackroute.button").wait(3).click()
            sleep(5)
            self.poco("iPhone").wait(3).click()
            # touch(Template(r"airplay\airplayipad.png", target_pos=5))
            sleep(10)
            touch([20,40])
        except Exception as e:
            print(e.args)
            print("youtube airplay execute fail")
            # snapshot(
            #     self.log_file_path + '\{0}-Youtube airplay execute fail.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S')),
            #     quality=30)

    def temp(self):
        name = self.poco("id.mdx.playbackroute.button").get_text()
        print(name)


if __name__ == '__main__':
    Y = AIRPLAY()
    while True:
        # X.APPlaunch("start","YouTube")

        # Y.youtubeairplay("the world in hdr in 4k", 30)
        # X.APPlaunch("stop", "youtube")

        Y.APPlaunch("start", "AppleTV")
        Y.appletvairplay("Elysium", 30)
        Y.APPlaunch("stop", "AppleTV")
        #
        # X.APPlaunch("start", "youtube")
        # Y.youtubecast("the world in hdr in 4k", 30)
        # X.APPlaunch("stop", "YouTube")
        #
        # X.APPlaunch("start", "Netflix")
        # Y.netflixuser()
        # Y.netflixcast("MY OCTOPUS TEACHER", 30)
        # X.APPlaunch("stop", "Netflix")
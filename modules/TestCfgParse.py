
#import chardet
import configparser
import os

log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__))+'/Config')
AutoTestAppINI = log_file_path + '/AutoTestApp.INI'
# print(log_file_path)

class myconf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    # 这里重写了optionxform方法，直接返回选项名
    def optionxform(self, optionstr):
        return optionstr

class TestCfgParse(object):

    def GetTestCfgInfo(self,cfgItem):
        cfgList = ''
        try:            
            with open(AutoTestAppINI, 'r',encoding="UTF-8") as f:
                cfgList = [line.strip() for line in f.readlines()]
                # print(cfgList)
                #self.fileList                
                f.close()
        except:
            pass  
        #self.AutoTestInfoFile = 'Sanity_Test.xlsx'
        for item in cfgList:
            if item.startswith(cfgItem):
                return item.split("=")[1] 

class CfgParse(object):

    def __init__(self, file=None):
        self.file = file
        self.cf = self.load_init(self.file)


    def load_init(self,file):
        cf = myconf()
        cf.read(file, encoding="utf-8")
        return cf

    def GetCfgInfo(self,section,cfgitem):
        try:
            return self.cf.get(section,cfgitem)
        except Exception as e:
            print(e.args)

    def SetCfgInfo(self, section, cfgitem, revise):
        try:
            return self.cf.set(section, cfgitem, revise)
        except Exception as e:
            print(e.args)

    def Reloadini(self):
        self.cf.write(open(self.file,"w",encoding="utf-8"))

if __name__ == "__main__":
    
    
    # CameraCfg=TestCfgParse()
    CameraCfg=CfgParse(AutoTestAppINI)
    CameraVDN=CameraCfg.GetCfgInfo("RestConnection","Ethernet.IP")
    CameraADN=CameraCfg.GetCfgInfo("Camera","Camera_Audio_Device_Name")
    RedRatdate = CameraCfg.GetCfgInfo("AUTOTEST","AutoTestCfg")
    print(RedRatdate)
    print(CameraVDN)
    print(CameraADN)
    # CameraCfg.Reloadini()
    # CameraCfg.GetCfgInfo("Camera","Camera_Video_Device_Name","sadad")
    # CameraCfg.Reloadini()
    # config = configparser.ConfigParser()
    # config.read(AutoTestAppINI, encoding="utf-8")
    # print(config.sections())
    # r = config.options("Camera")
    # r = config.get("Camera","Camera_Audio_Device_Name")
    # print(r)
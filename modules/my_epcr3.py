
# -*- coding: utf-8 -*- 
import requests
from modules.TestCfgParse import TestCfgParse

class PowerController(object):
    def _init_(self):
        pass


    def control_power(self,outlet,status): 
        
        # Get test configuration                 
        epcr3Cfg = TestCfgParse()
        epcr3_ip = epcr3Cfg.GetTestCfgInfo('EPCR3_IP') #EPCR3 IP Address
        print(("EPCR3 IP address:",epcr3_ip))
        username=epcr3Cfg.GetTestCfgInfo('EPCR3_UserName') # username
        print("EPCR3 Username:", username)
        password=epcr3Cfg.GetTestCfgInfo('EPCR3_PW') # password
        print(("Dictionary File:",password))
                

        # Connecting to power controller
        response_flag=0
        url = 'http://' + epcr3_ip + '/outlet?' + outlet + '=' + status
        if response_flag==0:
            try:
                response=requests.get(url, auth=(username,password), timeout=3)
                response.raise_for_status()
            except requests.exceptions.HTTPError as httpErr:
                print(("Http Error:",httpErr)) 
            except requests.exceptions.ConnectionError as connErr:
                print(("Error Connecting:",connErr)) 
            except requests.exceptions.Timeout as timeOutErr:
                print(("Timeout Error:",timeOutErr))
            except requests.exceptions.RequestException as reqErr:
                print(("Something Else:",reqErr))
            requests.get(url, timeout=3)
            response_flag=1
        else:
            try:
                response=requests.get(url, timeout=3)
                response.raise_for_status()
            except requests.exceptions.HTTPError as httpErr: 
                print(("Http Error:",httpErr)) 
            except requests.exceptions.ConnectionError as connErr: 
                print(("Error Connecting:",connErr)) 
            except requests.exceptions.Timeout as timeOutErr: 
                print(("Timeout Error:",timeOutErr)) 
            except requests.exceptions.RequestException as reqErr: 
                print(("Something Else:",reqErr))




if __name__=='__main__':
    Controller = PowerController()
    Controller.control_power('1','CCL')









#!/usr/bin/env python
import os

import requests
import json
import threading
import queue
import subprocess
import time
import simplejson
import urllib3

from modules.TestCfgParse import TestCfgParse,CfgParse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__))+'/Config')
AutoTestAppINI = log_file_path + '/AutoTestApp.INI'

restCfg = CfgParse(AutoTestAppINI)
dutIP = restCfg.GetCfgInfo("RestConnection","Ethernet.IP") #DUT IP Address
print("DUT IP address:",dutIP)
PORT=restCfg.GetCfgInfo("RestConnection","Port") # REST Port
print("REST Port:",PORT)
DICT_FILE=restCfg.GetCfgInfo("RestConnection","DICT_FILE") # Rest Dictionary
print("Dictionary File:",DICT_FILE)


RESTLOG_FILE = "../Restlog/"
DEVICE_NAME = "TABLET"
DEVICE_ID = "1234567890"
HEADERS = {"Content-Type": "application/json"}
PAIR = False
DEFAULT = True
dict = {}

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

class restterminal():
    def __init__(self):
        pass
    def pair(self):
        print("Pairing with device...")
        # force requires_pairing and enforce_auth_token to be true
        #start adb logcat thread
        subprocess.call(["adb", "disconnect"], shell=True)
        subprocess.call(["adb", "connect", dutIP], shell=True)
        process = subprocess.Popen(["adb", "-s", dutIP+":5555", "shell", "logcat"], stdout=subprocess.PIPE, shell=True)
        stdout_queue = queue.Queue()
        stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.start()

        # find challenge_type and req_token
        uri = "https://" + dutIP + ":" + PORT + "/pairing/start"
        payload = json.dumps({"DEVICE_ID": DEVICE_ID, "DEVICE_NAME": DEVICE_NAME})
        result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
        print (result)
        if result["STATUS"]["RESULT"] != "SUCCESS":
            print(("Can't connect to TV. STATUS: %s" % result["STATUS"]["RESULT"]))
            #exit(1)
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
                    uri = "https://" + dutIP + ":" + PORT + "/pairing/pair"
                    payload = json.dumps({"DEVICE_ID": DEVICE_ID, "CHALLENGE_TYPE": challenge_type,
                            "RESPONSE_VALUE": challenge_pin, "PAIRING_REQ_TOKEN": req_token})
                    result = requests.put(uri, verify=False, data=payload, headers=HEADERS).json()
                    print (result)
                    if(result["STATUS"]["RESULT"] == "SUCCESS"):
                        return result["ITEM"]["AUTH_TOKEN"]
                    
    def read_dictionary(self):
        global dict
        file = open(DICT_FILE, 'r')

        dict = {}
        for line in file:
            # skip commented line or empty lines
            if line[0] == "#" or line[0] == "\n":
                continue
            # grab dynamic uri and put into dictionary
            partial_uri, key = line.split(" ", 1)
            key = key.rstrip().lower()
            dict[key] = "https://" + dutIP + ":" + PORT + partial_uri

    def parse_command(self,line,auth_token):
        global result_json
        global items_value
        print (line)
        values = line.split(" ")
        command = ""
        if len(values) > 0:
            command = values[0]       
        if len(values) > 1:
            values = values[1:]            
        else:
            values = []
       
        silent = False
        for value in values:
            print(('value is:%s',value))
            if value == "-s":
                silent = True
                values.remove("-s")           
            
        # dynamic get
        if command.lower() == "get":
            if not silent:
                print(line)

            uri = dict[values[0].lower()]
            
            print(uri)           
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            result_json = requests.get(uri, verify=False, headers={"AUTH": auth_token}).json()
            #print (command.lower())     
            if not silent:
                print((json.dumps(result_json, indent=4, separators=(',', ': '))))
                items_value = result_json["ITEMS"][0]["VALUE"]
                print(items_value)
                return items_value
                
            if "STATUS" not in result_json or "RESULT" not in result_json["STATUS"] or result_json["STATUS"]["RESULT"] != "SUCCESS":
                print("the case failed")
                return False
            else:
                print("the case is Pass")
                return result_json

        # static get
        elif command.lower() == "gets":
            if not silent:
                print(line)

            uri = dict[values[0].lower()].replace("dynamic", "static")
            requests.packages.urllib3.disable_warnings()
            result_json = requests.get(uri, verify=False, headers={"AUTH": auth_token}).json()
            print(result_json)
                    
            if not silent:
                print((json.dumps(result_json, indent=4, separators=(',', ': '))))
                items_value = result_json["ITEMS"][0]["VALUE"]
                print(items_value)
                return items_value

            if "STATUS" not in result_json or "RESULT" not in result_json["STATUS"] or result_json["STATUS"]["RESULT"] != "SUCCESS":
                print("The case is Fail")
                return False
            else:
                print("The case is Pass")
                return result_json

        elif command.lower() == "put":
            print(line)
            key = values[0]

            # grab value for put
            value = ""
            if len(values) > 1:
                value = values[1]
                if len(values) > 2:
                    for temp in values[2:]:
                        value = value + " " + temp
            uri = dict[key.lower()]
            dyn_comm="get " + key + " -s"
            sta_comm="gets " + key + " -s"
            dynamic_json = self.parse_command(dyn_comm,auth_token)
            static_json = self.parse_command(sta_comm,auth_token)
            print(dynamic_json)

            if not dynamic_json or not static_json:
                print("it's blocked due to not dynamic_json or static_json")
                return False

            # grab type, and check if READONLY
            if key == "current_state" or key == "start_update":
                type = dynamic_json["ITEM"]["TYPE"]
                #print type
            else:
                # special read-only cases
                if key == "wireless_access_points":
                    print("it's NA key equal to wireless_access_points")
                    return True
                elif key[:3] == "msi" or key[:3] == "nhi":
                    print("it's msi or nhi")
                    return True

                if "ITEMS" in dynamic_json and isinstance(dynamic_json["ITEMS"], list) and len(dynamic_json["ITEMS"]) > 0:
                    if "READONLY" in dynamic_json["ITEMS"][0] and dynamic_json["ITEMS"][0]["READONLY"] == "TRUE":
                        print("It's NA READONLY")
                        return True
                else:
                    print("it's blocked")
                    return False
                if "ITEMS" not in static_json or not isinstance(static_json["ITEMS"], list) or len(static_json["ITEMS"]) <= 0:
                    print("it's blocked due to ITEMS not in static_json")
                    return False

                if "TYPE" in dynamic_json:
                    type = dynamic_json["TYPE"]
                else:
                    if "TYPE" not in dynamic_json["ITEMS"][0]:
                        print("It's blocked due to TYPE not in dynamic_json")
                        return False
                    type = dynamic_json["ITEMS"][0]["TYPE"]

            if type == "T_ACTION_V1":
                if value != "":
                    if "HASHVAL" in dynamic_json["ITEMS"][0]:
                        hashval = dynamic_json["ITEMS"][0]["HASHVAL"]
                        payload = json.dumps({"REQUEST": "ACTION", "VALUE": value, "HASHVAL": hashval})
                        print("payload")
                        print(payload)
                    else:
                        payload = json.dumps({"REQUEST": "ACTION", "VALUE": value})
                        print("payload2")
                        print(payload)
                else:
                    if "HASHVAL" in dynamic_json["ITEMS"][0]:
                        hashval = dynamic_json["ITEMS"][0]["HASHVAL"]
                        print(hashval)
                        payload = json.dumps({"REQUEST": "ACTION", "HASHVAL": hashval})
                    else:
                        payload = json.dumps({"REQUEST": "ACTION"})

                result_json = requests.put(uri, verify=False, data=payload, headers={"Content-Type": "application/json", "AUTH": auth_token}).json()
                print((json.dumps(result_json, indent=4, separators=(',', ': '))))
                #print (json.dumps(result_json, indent=4, separators=(',', ': ')))["PARAMETERS"]["VALUE"]
                test = True
                if "STATUS" not in result_json or "RESULT" not in result_json["STATUS"] or result_json["STATUS"]["RESULT"] != "SUCCESS":
                    test = False
            else:
                cases = []

                # type cast value if necessary, then add list to the list
                if value != "":
                    if type == "T_VALUE_V1" or type == "T_VALUE_ABS_V1":
                        value = int(value)
                    if type == "T_AP_V1" or type == "T_DEVICE_V1":
                        value = json.loads(value)

                    cases.append(value)

                # if value is unspecified, check type and add default check values to the list
                else:
                    if type == "T_MENU_V1" or type == "T_STRING_V1" or type == "T_MATRIX_V1" or type == "T_HEADER_V1" or type == "T_ROW_V1" or type == "T_LIST_CEC_DEVICE_V1":
                        print("it's NA")
                        return True
                    elif type == "T_VALUE_V1" or type == "T_VALUE_ABS_V1":
                        if "MAXIMUM" not in static_json["ITEMS"][0] or "MINIMUM" not in static_json["ITEMS"][0]:
                            print("it's blocked due to MaXIUMU not in static_json")
                            return False

                        cases.append(static_json["ITEMS"][0]["MAXIMUM"])
                        cases.append(static_json["ITEMS"][0]["MINIMUM"])

                        if type == "T_VALUE_ABS_V1":
                            if "CENTER" not in static_json["ITEMS"][0]:
                                print("it's blocked due to CENTER not in static_json")
                                return False
                            else:
                                cases.append(static_json["ITEMS"][0]["CENTER"])
                    elif type == "T_LIST_X_V1":
                        if "ELEMENTS" not in dynamic_json["ITEMS"][0]:
                            print("it's blocked due to ELEMENTS not in dynamic_json")
                            return False

                        for element in dynamic_json["ITEMS"][0]["ELEMENTS"]:
                            cases.append(element)
                    elif type == "T_LIST_V1":
                        if "ELEMENTS" not in static_json["ITEMS"][0]:
                            print("ELEMENTS not in static_json")
                            return False

                        for element in static_json["ITEMS"][0]["ELEMENTS"]:
                            cases.append(element)
                    elif type == "T_DEVICE_V1":
                        cases.append({"NAME": "Test", "METADATA": "Metadata"})

                test = True
                for case in cases:
                    dyn_comm1="get " + key + " -s"
                    dynamic_json = self.parse_command(dyn_comm1,auth_token)
                    if key != "current_state" and "HASHVAL" in dynamic_json["ITEMS"][0]:
                        hashval = dynamic_json["ITEMS"][0]["HASHVAL"]
                        payload = json.dumps({"REQUEST": "MODIFY", "VALUE": case, "HASHVAL": hashval})
                    else:
                        payload = json.dumps({"REQUEST": "MODIFY", "VALUE": case})
                    result_json = requests.put(uri, verify=False, data=payload, headers={"Content-Type": "application/json", "AUTH": auth_token}).json()
                    print((json.dumps(result_json, indent=4, separators=(',', ': '))))

                    if "STATUS" not in result_json or "RESULT" not in result_json["STATUS"] or result_json["STATUS"]["RESULT"] != "SUCCESS":
                        test = False

            if test:
                print("it's Pass")
                return result_json
            else:
                print("it's Fail")
                return False

        elif command.lower() == "delete_custom_picture_modes":
            print(line)

            dynamic_json = self.parse_command("get picture_mode", auth_token)
            if "ITEMS" not in dynamic_json or not isinstance(dynamic_json["ITEMS"], list) or len(dynamic_json["ITEMS"]) <= 0 or "ELEMENTS" not in dynamic_json["ITEMS"][0]:
                return False

            for picture_mode in dynamic_json["ITEMS"][0]["ELEMENTS"][6:]:
                self.parse_command("put picture_mode ",auth_token)
                self.parse_command("put delete_picture_mode " + picture_mode)
            return True

        elif command.lower() == "wait":
            print(line)
            time.sleep(float(values[0]))
            return True

        elif command.lower() == "restlog":
            if len(values) > 0:
                restlog_file = RESTLOG_FILE + values[0]
            else:
                restlog_file = RESTLOG_FILE + "./Logs/restlog.txt"

            uri = "https://" + dutIP + ":" + PORT + "/restlog"
            dynamic_json = requests.get(uri, verify=False).text.replace("<pre>", "").replace("</pre>", "")

            file = open(restlog_file, 'w')
            file.write(dynamic_json)
            file.close()
            return True

        elif command.lower() == "exit":
            exit(0)

if __name__ == "__main__":
    global auth_token
    rest = restterminal()
    auth_token = rest.pair()
    print(auth_token)
    rest.read_dictionary()
    requests.packages.urllib3.disable_warnings()
    rest.parse_command("put factory_reset",auth_token)
    #rest.parse_command("restlog",auth_token)

   


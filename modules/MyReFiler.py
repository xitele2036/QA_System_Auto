import json
import re
import os

class ReFilter(object):
    def txtFilter(self,fileName,keyWord):
        print(keyWord)
        # if '' in keyWord:
        #     #pattern= ".".join(keyWord.split())
        #     pattern= keyWord.replace(" ",".")
        #     print('pattern is')
        #     print(pattern)
        #     print('finish')
            
        new_lines=[]

        try:
            f = open(fileName,'r',encoding="UTF-8")
            for eachLine in f.readlines():
                # print re.split('\s\s+',eachLine)
                m = re.search(keyWord, eachLine)
                # print(m)


                # m=re.match(keyWord,eachLine)
                # m=re.findall(keyWord,eachLine)
                # print m
                if m is not None:
                    return m.group()
            f.close()
        except IOError as e:
            print('ERROR: could not open file',e)        
        
    def getAirplayCode(self,fileName):
        regex = r'"pin" : .*'
        with open(fileName, 'r',encoding="UTF-8") as f:
            # print(f.read())
            n = re.findall(regex,f.read(),re.IGNORECASE)
        # print(n[0])
        codes = n[-1].replace('"','')
        code = codes.split(':')
        # print(code[1])
        return code[-1]



        
if __name__ == "__main__":
    mytxtfilter=ReFilter()
    code = mytxtfilter.getAirplayCode('./Logs/SSHlogcat.log')
    print(code)
    # v=mytxtfilter.txtFilter('.\Logs\P759_PM.txt','"pin" : ')
    # print(v)
    # if v is not None:
    #     print(True)
    # else:
    #     print(False)
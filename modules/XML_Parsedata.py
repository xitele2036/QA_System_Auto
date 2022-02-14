# -*- coding: utf-8 -*-
import xml.dom.minidom
import math
class XML_PARSE():
        def __init__(self):
                pass       
        def Parameter(self,filename,MacroName):
                 
                #Use minidom to open xlm file
                DOMTree = xml.dom.minidom.parse(filename)
                MacroArray=DOMTree.getElementsByTagName("ArrayOfMacro")[0].childNodes
                
                #Get the number of macros            
                MacroNum=MacroArray.length/2
                print("MacroNumber:",MacroNum)
                
                i=0               
                while i< MacroNum:
                        
                        Macro = DOMTree.getElementsByTagName("Macro")[i].childNodes
                        print(Macro.length)
                        
                        # The name of macro is at the 5th node
                        if MacroName==Macro[5].childNodes[0].data:
                                
                                # MacroActions is at the 7th node of Macro, get MacroActions list
                                MacroActions = Macro[7].childNodes
                                print("MacroActions:",MacroActions)
                                print("MacroActions Length:",Macro[7].childNodes.length)
                
                                n=1
                                SignalSeq=[]
                                while (n < Macro[7].childNodes.length):
                                                
                                        print("MacroAction length:",MacroActions[n].childNodes.length)
                                        #get MacroAction nodelist
                                        MacroAction=MacroActions[n].childNodes
                                        print("MacroAction:",MacroAction)
                                        #Get IR signal delay time (s)
                                        SignalPauseTime=int(MacroAction[1].childNodes[0].data)/1000
                                        print("signalPausetime(s):",SignalPauseTime)
                                        
                                        #Get IR signal, IR signal is at the 9th node of MacroAction
                                        Signal=MacroAction[9].getElementsByTagName('Name')[0].childNodes[0].data
                                        print("Signal:",Signal)
                                         
                                        #Generate the sigle and signal sequence list
                                        Signal_Pause=[Signal,SignalPauseTime]

                                        SignalSeq=SignalSeq+Signal_Pause
                                        print("Signal Sequence:",SignalSeq)
                        
                                        n+=2
                                        print("n=",n)   
                        i+=1
                        print("i:",i)
                        
                if SignalSeq !=[]:
                        return SignalSeq
                
        

if __name__ == "__main__":
        auto = XML_PARSE()

        Value =auto.Parameter('MacroList.xml','menu')
        print(Value)







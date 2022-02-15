import wx.html


class VsiliconAbout(wx.Dialog):
    text ='''
    <html>
    <body bgcolor="#ACAA60">
    <center><table bgcolor="#455481" width="100%" cellspacing="0"
    cellpadding="0" border="1">
    <tr>
    <td align="center"><h1>AutoTestApp</h1></td>
    </tr>
    </table>
    </center>
    Develop Envirnoment: Python-3.9.0<br/>

    Run AutoTestApp.exe to start your testing<br/>
    
    <p><h4>1.Test case Management:</h4><br/>
      All test cases are managed by Excel, the default test case is "Sanity_Test.xlsx", Here is the the simple description for every field.<br/>
      &nbsp&nbsp- Case_Available: 1- available for test	<br/>
      &nbsp&nbsp- Rest_Control: "PAIR" is for rest PAIR, command is in "Rest_Command.xlsx"	<br/>
      &nbsp&nbsp- IR_Seq: IR command sequence for RedRat control such as "menu,2" means that press menu key and wait for 2s, if the string includes ".xml" which could record with redrat, then it could execute the test sequence.<br/>
      &nbsp&nbsp- SerialCmd: Serialcommand for DUT serial port	<br/>
      &nbsp&nbsp- EQ_QD_Control: command for QuantamData control <br/>
      &nbsp&nbsp- EQ_Streamer_Control: Command for streamer Control (TBD)	<br/>
      &nbsp&nbsp- Log_Capture:keyword what you want to get from log	<br/>
      &nbsp&nbsp- Log_Ref:the expected result	<br/>
      &nbsp&nbsp- PIC_Capture: the picture name do you want to capture.	<br/>
      &nbsp&nbsp- PIC_Ref: expected reference PIC name <br/>
      &nbsp&nbsp- Audio_Capture: Audio information from log	<br/>
      &nbsp&nbsp- Audio_Ref: expected audio result	<br/>
      &nbsp&nbsp- PIC_Result: comparasion result	<br/>
      &nbsp&nbsp- Audio_Result: comparation result	<br/>
      &nbsp&nbsp- Test Result: overall test result    <br/></p>
    
    <p><h4>2.Setup the test envirnoment: connect the test equipment to test PC and DUT. </h4><br/>
      Test equipment support list: QuantumData generator(UART control) UART for HDMI, RedRat for IR control which need start Redrat hub agent, UniGRAF UCD-2 Vx1 for Vx1 video capture. <br/></p>
    
    <p><h4>3.Edit "AutoTestApp" </h4><br/>
      text file to do configuration before testing such as DUT's IP and Port, DUT's Serial Port, Test PC IP for Red Rat communication and QD generator Serial port.  <br/></p>
    
    <p><h4>3.Run AutoTestApp   </h4><br/>
      &nbsp&nbsp(1)select the test cases by double click the test case tree or individual test case that you want to do.  <br/>
         Example: select SWU_001 - SW upgrade from UART <br/>
                         Pair_001 - do system pair  <br/>
                         Input_004 - Switch source to HDMI4, change timing and pattern, then capture a image with UCD-2 and then do image comparision   <br/>
       
      &nbsp&nbsp(2)Run individual case - select 1 case with case_available=1, and click "Run" button  <br/>
      &nbsp&nbsp(3)Run a group of test case- select multiple test cases which their case_available should be 1, and select Loop to run a group of test cases. Or click "select All" to run all cases. <br/></p>
      
    <p><h4>4. Test Report- Test Result will be written in "Sanity_test.xlsx"   </h4><br/> </p>
    <center><p>Copyright
    &copy; 1997-2022.</p>
    </center>
    </body>
    </html>
    '''

    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,'About',size=(800,600))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self,wx.ID_OK,"Okay")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html,1,wx.EXPAND|wx.ALL,5)
        sizer.Add(button,0,wx.ALIGN_CENTER|wx.ALL,5)

        self.SetSizer(sizer)
        self.Layout()

# app = wx.App()
# frm = VsiliconAbout(None)
# frm.Show()
# app.MainLoop()